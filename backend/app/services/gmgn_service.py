from typing import List, Dict, Any, Optional # Add Optional if you use it for type hints too
import time
import pandas as pd
from curl_cffi.requests import Session, BrowserType, RequestsError # Make sure Session is imported if used as a type hint
from app.core.config import settings
from app.models.pydantic_models import TokenPerformanceData, WalletSummary, MasterCopyPerformance
import asyncio
from app.core.config import settings
from app.models.pydantic_models import TokenPerformanceData, WalletSummary, MasterCopyPerformance

def to_float_safe(value, default=0.0):
    if value is None: return default
    try: return float(value)
    except (ValueError, TypeError): return default

def calculate_pnl_percentage_raw(pnl, cost):
    pnl_f = to_float_safe(pnl)
    cost_f = to_float_safe(cost)
    if cost_f != 0:
        return (pnl_f / cost_f) * 100 if cost_f > 0 else (pnl_f / 0.000001) * 100
    return 0 if pnl_f == 0 else float('inf') if pnl_f > 0 else float('-inf')

def calculate_current_mcap_raw(token_price, total_supply):
    price = to_float_safe(token_price)
    supply = to_float_safe(total_supply)
    if price > 0 and supply > 0:
        return price * supply
    return 0

async def fetch_wallet_data_from_gmgn(wallet_address: str, session: Session) -> List[Dict[str, Any]]:
    url = f"{settings.GMGN_API_BASE_URL}{wallet_address}"
    try:
        response = await session.get(url, params=settings.GMGN_API_PARAMS) # Use await for async session
        response.raise_for_status()
        data = response.json()
        if data.get("code") == 0 and "data" in data and "holdings" in data["data"]:
            return data["data"]["holdings"]
        print(f"GMGN API Error for {wallet_address}: {data.get('message', 'Unknown error')}")
        return []
    except RequestsError as e:
        print(f"HTTP Request Error (gmgn) {wallet_address}: {e}")
        return []
    except Exception as e:
        print(f"Generic Error (gmgn) {wallet_address}: {e}")
        return []

async def process_wallet_performance_data(
    main_wallet_address: Optional[str],
    master_wallet_addresses: List[str]
) -> Dict[str, Any]:
    
    all_fetched_wallets_summary: List[WalletSummary] = []
    all_fetched_tokens_raw: List[Dict] = [] # Store raw token data with wallet_address_ref

    wallets_to_process = []
    if main_wallet_address:
        wallets_to_process.append({"address": main_wallet_address, "alias": "My Wallet (Main)", "is_main": True})
    
    unique_master_addresses = set(master_wallet_addresses)
    if main_wallet_address in unique_master_addresses:
         unique_master_addresses.remove(main_wallet_address)

    for addr in unique_master_addresses:
        wallets_to_process.append({"address": addr, "alias": addr[:6]+"..."+addr[-4:], "is_main": False})

    # Use a single async session
    async with Session(
        impersonate=BrowserType(settings.GMGN_BROWSER_IMPERSONATE), # curl_cffi async needs explicit BrowserType
        headers=settings.GMGN_API_HEADERS,
        http_version=2 # Often needed for impersonation stability
    ) as session:
        for i, wallet_info in enumerate(wallets_to_process):
            addr = wallet_info["address"]
            print(f"Fetching for: {addr}")
            raw_holdings = await fetch_wallet_data_from_gmgn(addr, session)
            
            w_total_pnl, w_realized_pnl, w_unrealized_pnl = 0.0, 0.0, 0.0
            w_total_cost, w_total_sold = 0.0, 0.0
            w_tokens_count, w_profitable_tokens = 0, 0
            w_last_active_ts = 0

            if raw_holdings:
                w_tokens_count = len(raw_holdings)
                for token_item_raw in raw_holdings:
                    # Directly create TokenPerformanceData Pydantic model instance
                    # The alias in Pydantic model handles mapping 'token' from gmgn to 'token_info'
                    try:
                         token_perf = TokenPerformanceData(
                             **token_item_raw, # Spread the raw item
                             wallet_address_ref=addr,
                             is_main_wallet_token=wallet_info["is_main"]
                         )
                    except Exception as p_err:
                        print(f"Pydantic validation error for token in {addr}: {p_err}, item: {token_item_raw.get('token',{}).get('symbol')}")
                        continue # Skip this token if parsing fails

                    token_pnl = to_float_safe(token_perf.total_profit)
                    w_total_pnl += token_pnl
                    w_realized_pnl += to_float_safe(token_perf.realized_profit)
                    w_unrealized_pnl += to_float_safe(token_perf.unrealized_profit)
                    w_total_cost += to_float_safe(token_perf.history_bought_cost)
                    w_total_sold += to_float_safe(token_perf.history_sold_income)
                    if token_pnl > 0: w_profitable_tokens +=1
                    if token_perf.last_active_timestamp and token_perf.last_active_timestamp > w_last_active_ts:
                        w_last_active_ts = token_perf.last_active_timestamp
                    
                    # Add calculated fields
                    token_perf.pnl_percentage = calculate_pnl_percentage_raw(token_perf.total_profit, token_perf.history_bought_cost)
                    token_perf.current_mcap = calculate_current_mcap_raw(
                        token_perf.token_info.current_token_price, token_perf.token_info.current_total_supply
                    )
                    all_fetched_tokens_raw.append(token_perf) # Store Pydantic model instance

            all_fetched_wallets_summary.append(
                WalletSummary(
                    address=addr, alias=wallet_info["alias"], is_main_wallet=wallet_info["is_main"],
                    total_pnl=w_total_pnl, realized_pnl=w_realized_pnl, unrealized_pnl=w_unrealized_pnl,
                    total_cost_usd=w_total_cost, total_sold_income_usd=w_total_sold,
                    tokens_traded_count=w_tokens_count, profitable_tokens_count=w_profitable_tokens,
                    last_activity_timestamp=w_last_active_ts or None,
                    profitable_token_rate = (w_profitable_tokens / w_tokens_count * 100) if w_tokens_count > 0 else 0.0
                )
            )
            if i < len(wallets_to_process) - 1:
                await asyncio.sleep(settings.API_CALL_DELAY_SECONDS) # Use asyncio.sleep

    # Separate tokens for main and master wallets
    my_wallet_tokens_list = [t for t in all_fetched_tokens_raw if t.is_main_wallet_token]
    master_wallets_tokens_list = [t for t in all_fetched_tokens_raw if not t.is_main_wallet_token]
    my_wallet_summary_obj = next((w for w in all_fetched_wallets_summary if w.is_main_wallet), None)
    master_wallets_summary_list = [w for w in all_fetched_wallets_summary if not w.is_main_wallet]

    # Calculate MasterCopyPerformance (Screenshot 1 logic)
    master_copy_perf_list: List[MasterCopyPerformance] = []
    if my_wallet_tokens_list and master_wallets_summary_list:
        df_my_tokens = pd.DataFrame([t.model_dump() for t in my_wallet_tokens_list]) # Convert Pydantic to dict for Pandas
        if not df_my_tokens.empty:
             df_my_tokens['token_address'] = df_my_tokens['token_info'].apply(lambda x: x.get('address') if isinstance(x, dict) else None)


        for master_summary in master_wallets_summary_list:
            current_master_tokens = [
                t.model_dump() for t in master_wallets_tokens_list if t.wallet_address_ref == master_summary.address
            ]
            if not current_master_tokens or df_my_tokens.empty:
                master_copy_perf_list.append(MasterCopyPerformance(master_wallet_alias=master_summary.alias, master_wallet_address=master_summary.address))
                continue

            df_master_tokens_current = pd.DataFrame(current_master_tokens)
            df_master_tokens_current['token_address'] = df_master_tokens_current['token_info'].apply(lambda x: x.get('address') if isinstance(x, dict) else None)

            common_tokens_df = pd.merge(
                df_my_tokens[['token_address', 'total_profit', 'history_sold_income', 'history_bought_cost']],
                df_master_tokens_current[['token_address', 'total_profit']],
                on='token_address', suffixes=('_my', '_master')
            )
            
            num_common = len(common_tokens_df)
            my_income = common_tokens_df['total_profit_my'].apply(to_float_safe).sum() if num_common > 0 else 0.0
            # ... (rest of common token calculations for inflow, outflow, wins etc.) ...
            # For brevity, I'll just pass the main income. You can expand this.
            master_copy_perf_list.append(MasterCopyPerformance(
                master_wallet_alias=master_summary.alias,
                master_wallet_address=master_summary.address,
                num_common_tokens=num_common,
                my_income_common_usd=my_income
                # ... populate other MasterCopyPerformance fields ...
            ))
            
    return {
        "my_wallet_summary": my_wallet_summary_obj,
        "my_wallet_tokens": my_wallet_tokens_list,
        "master_wallets_summary": master_wallets_summary_list,
        "master_copy_performance": master_copy_perf_list,
        "all_master_wallets_tokens": master_wallets_tokens_list
    }

import asyncio # Add this at the top of gmgn_service.py