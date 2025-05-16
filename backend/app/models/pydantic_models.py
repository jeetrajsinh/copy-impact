# backend/app/models/pydantic_models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class TokenInfo(BaseModel):
    address: Optional[str] = None
    symbol: Optional[str] = None
    name: Optional[str] = None
    logo: Optional[str] = None
    current_token_price: Optional[float] = Field(None, alias="price") # From gmgn token object
    current_total_supply: Optional[float] = Field(None, alias="total_supply") # From gmgn token object

class TokenPerformanceData(BaseModel):
    token_info: TokenInfo = Field(..., alias="token") # Mapped from gmgn
    wallet_address_ref: Optional[str] = None # Added by our service
    is_main_wallet_token: Optional[bool] = False # Added by our service

    total_profit: Optional[float] = 0.0
    realized_profit: Optional[float] = 0.0
    unrealized_profit: Optional[float] = 0.0
    history_bought_cost: Optional[float] = 0.0
    history_sold_income: Optional[float] = 0.0
    avg_cost: Optional[float] = 0.0
    avg_sold: Optional[float] = 0.0
    last_active_timestamp: Optional[int] = None
    # Include other fields from gmgn as needed and map them
    # e.g. balance: Optional[str] = None (gmgn provides as string)
    
    # Fields calculated by our service
    pnl_percentage: Optional[float] = None
    current_mcap: Optional[float] = None
    
    class Config:
        populate_by_name = True # Allows using alias for 'token'

class WalletSummary(BaseModel):
    address: str
    alias: str
    is_main_wallet: bool
    total_pnl: float = 0.0
    realized_pnl: float = 0.0
    unrealized_pnl: float = 0.0
    total_cost_usd: float = 0.0
    total_sold_income_usd: float = 0.0
    tokens_traded_count: int = 0
    profitable_tokens_count: int = 0
    last_activity_timestamp: int = 0
    # Add WR% if you define it clearly
    # Profitable Token Rate (%)
    profitable_token_rate: float = 0.0

class MasterCopyPerformance(BaseModel): # For Screenshot 1 type data
    master_wallet_alias: str
    master_wallet_address: str
    num_common_tokens: int = 0
    master_wins_common: int = 0 # Master's wins on common tokens
    my_wins_common: int = 0    # Your wins on common tokens
    my_inflow_common_usd: float = 0.0  # Your inflow from these common tokens
    my_outflow_common_usd: float = 0.0 # Your outflow for these common tokens
    my_income_common_usd: float = 0.0  # Your P&L from these common tokens
    my_wr_common_percentage: float = 0.0 # Your WR% on these common tokens

class PerformanceAnalysisRequest(BaseModel):
    main_wallet_address: str
    master_wallet_addresses: list[str]

class PerformanceAnalysisResponse(BaseModel):
    main_wallet_summary: WalletSummary
    master_wallets_performance: list[MasterCopyPerformance]
    main_wallet_tokens: list[TokenPerformanceData]
    master_wallets_tokens: dict[str, list[TokenPerformanceData]]