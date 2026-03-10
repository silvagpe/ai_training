// Analysis Result Models

export type RecommendationAction = 'HOLD' | 'BUY' | 'SELL';

export interface AssetAnalysis {
  ticker: string;
  name: string;
  fund_type: string;
  segment: string;
  action: RecommendationAction;
  current_price: number;
  dy_pct: number;
  price_to_book: number;
  reason: string;
  source: string;
  weight_recommended_pct?: number;
}

export interface PortfolioRecommendation {
  hold_assets: AssetAnalysis[];
  buy_assets: AssetAnalysis[];
  sell_assets: AssetAnalysis[];
}

export interface BenchmarkComparison {
  portfolio_total_return_pct: number;
  benchmark_total_return_pct: number;
  outperformance_pct: number;
  portfolio_avg_monthly_pct: number;
  benchmark_avg_monthly_pct: number;
  periods_analyzed: number;
}

export interface AnalyticsMetrics {
  sharpe_ratio?: number;
  treynor_ratio?: number;
  portfolio_volatility_pct?: number;
  benchmark_comparison?: BenchmarkComparison;
  projected_value_5y_brl?: number;
}

export interface DiversificationSummary {
  type_distribution: { [key: string]: number };
  herfindahl_index: number;
  suggested_fii_count: number;
  concentration_level: string;
}

export interface AnalysisOutput {
  portfolio_analysis: PortfolioRecommendation;
  diversification_summary: DiversificationSummary;
  recommended_allocation: { [ticker: string]: number };
  analytics?: AnalyticsMetrics;
  executive_summary: string;
  detailed_report: string;
}

export interface AnalysisResponse {
  analysis: AnalysisOutput;
  executive_summary: string;
  detailed_report: string;
  review_feedback: string;
}
