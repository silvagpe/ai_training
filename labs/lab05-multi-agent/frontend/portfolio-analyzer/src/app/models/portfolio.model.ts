// Portfolio Input Models

export interface PortfolioAsset {
  ticker: string;
  quantity: number;
  current_price: number;
  entry_date?: string;
}

export interface PortfolioInput {
  client_id?: string;
  current_assets: PortfolioAsset[];
  total_patrimony_brl: number;
  monthly_contribution_brl?: number;
  investment_horizon_months?: number;
}
