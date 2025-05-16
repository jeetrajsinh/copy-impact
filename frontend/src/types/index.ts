// TypeScript type definitions (mirroring Pydantic)
// ...existing code...
// frontend/src/types/index.ts
export interface TokenInfo {
  address?: string;
  symbol?: string;
  name?: string;
  logo?: string;
  current_token_price?: number; // alias: "price"
  current_total_supply?: number; // alias: "total_supply"
}

export interface TokenPerformanceData {
  token_info: TokenInfo;
  wallet_address_ref?: string;
  is_main_wallet_token?: boolean;

  total_profit?: number;
  realized_profit?: number;
  unrealized_profit?: number;
  history_bought_cost?: number;
  history_sold_income?: number;
  avg_cost?: number;
  avg_sold?: number;
  last_active_timestamp?: number;
  
  pnl_percentage?: number;
  current_mcap?: number;
}

export interface WalletSummary {
  address: string;
  alias: string;
  is_main_wallet: boolean;
  total_pnl?: number;
  realized_pnl?: number;
  unrealized_pnl?: number;
  total_cost_usd?: number;
  total_sold_income_usd?: number;
  tokens_traded_count?: number;
  profitable_tokens_count?: number;
  last_activity_timestamp?: number;
  profitable_token_rate?: number;
}

export interface MasterCopyPerformance {
  master_wallet_alias: string;
  master_wallet_address: string;
  num_common_tokens?: number;
  master_wins_common?: number;
  my_wins_common?: number;
  my_inflow_common_usd?: number;
  my_outflow_common_usd?: number;
  my_income_common_usd?: number;
  my_wr_common_percentage?: number;
}

export interface PerformanceAnalysisRequestData {
  main_wallet_address?: string | null;
  master_wallet_addresses: string[];
}

export interface PerformanceAnalysisResponseData {
  my_wallet_summary?: WalletSummary | null;
  my_wallet_tokens: TokenPerformanceData[];
  master_wallets_summary: WalletSummary[];
  master_copy_performance: MasterCopyPerformance[];
  all_master_wallets_tokens: TokenPerformanceData[];
}

// If you use import type, you don't need to re-export the type. Just import as:
// import type { PerformanceAnalysisResponseData } from '../types';