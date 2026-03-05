import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AnalyticsMetrics, DiversificationSummary } from '../models/analysis.model';

@Component({
  selector: 'app-analytics-metrics',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './analytics-metrics.component.html',
  styleUrl: './analytics-metrics.component.css'
})
export class AnalyticsMetricsComponent {
  @Input() analytics?: AnalyticsMetrics;
  @Input() diversification!: DiversificationSummary;
  @Input() recommendedAllocation!: { [key: string]: number };

  getTypeDistributionEntries(): Array<{key: string, value: number}> {
    return Object.entries(this.diversification.type_distribution)
      .map(([key, value]) => ({ key, value }));
  }

  getRecommendedAllocationEntries(): Array<{key: string, value: number}> {
    return Object.entries(this.recommendedAllocation)
      .map(([key, value]) => ({ key, value }))
      .sort((a, b) => b.value - a.value);
  }

  getConcentrationColor(level: string): string {
    switch (level.toLowerCase()) {
      case 'baixa': return 'emerald';
      case 'media': return 'amber';
      case 'alta': return 'rose';
      default: return 'slate';
    }
  }

  formatNumber(num: number | undefined): string {
    if (num === undefined || num === null) return 'N/A';
    return num.toFixed(2);
  }

  formatCurrency(num: number | undefined): string {
    if (num === undefined || num === null) return 'N/A';
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(num);
  }
}
