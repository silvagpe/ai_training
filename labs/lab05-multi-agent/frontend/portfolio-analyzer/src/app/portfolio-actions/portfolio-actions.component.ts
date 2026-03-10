import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PortfolioRecommendation, AssetAnalysis } from '../models/analysis.model';

@Component({
  selector: 'app-portfolio-actions',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './portfolio-actions.component.html',
  styleUrl: './portfolio-actions.component.css'
})
export class PortfolioActionsComponent {
  @Input() portfolioAnalysis!: PortfolioRecommendation;

  getActionColor(action: string): string {
    switch (action) {
      case 'BUY': return 'emerald';
      case 'SELL': return 'rose';
      case 'HOLD': return 'amber';
      default: return 'slate';
    }
  }

  getActionIcon(action: string): string {
    switch (action) {
      case 'BUY': return '📈';
      case 'SELL': return '📉';
      case 'HOLD': return '⏸️';
      default: return '•';
    }
  }
}
