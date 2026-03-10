import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PortfolioFormComponent } from './portfolio-form/portfolio-form.component';
import { PortfolioActionsComponent } from './portfolio-actions/portfolio-actions.component';
import { AnalyticsMetricsComponent } from './analytics-metrics/analytics-metrics.component';
import { ReportsComponent } from './reports/reports.component';
import { PortfolioService } from './services/portfolio.service';
import { PortfolioInput } from './models/portfolio.model';
import { AnalysisResponse } from './models/analysis.model';

@Component({
  selector: 'app-root',
  imports: [
    CommonModule,
    PortfolioFormComponent,
    PortfolioActionsComponent,
    AnalyticsMetricsComponent,
    ReportsComponent
  ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('FII Portfolio Analyzer');
  
  isLoading = signal(false);
  analysisResult = signal<AnalysisResponse | null>(null);
  errorMessage = signal<string | null>(null);

  constructor(private portfolioService: PortfolioService) {}

  onSubmitPortfolio(portfolio: PortfolioInput): void {
    this.isLoading.set(true);
    this.errorMessage.set(null);
    this.analysisResult.set(null);

    this.portfolioService.analyzePortfolio(portfolio).subscribe({
      next: (result) => {
        this.analysisResult.set(result);
        this.isLoading.set(false);
        // Scroll to results
        setTimeout(() => {
          document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      },
      error: (error) => {
        this.errorMessage.set(error.message);
        this.isLoading.set(false);
      }
    });
  }
}
