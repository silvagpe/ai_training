import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './reports.component.html',
  styleUrl: './reports.component.css'
})
export class ReportsComponent {
  @Input() executiveSummary!: string;
  @Input() detailedReport!: string;
  @Input() reviewFeedback!: string;

  showDetailedReport = false;
  showReviewFeedback = false;

  toggleDetailedReport(): void {
    this.showDetailedReport = !this.showDetailedReport;
  }

  toggleReviewFeedback(): void {
    this.showReviewFeedback = !this.showReviewFeedback;
  }

  formatMarkdown(text: string): string {
    if (!text) return '';
    
    // Simple markdown to HTML conversion
    return text
      // Headers
      .replace(/^### (.*$)/gim, '<h3 class="theme-markdown-h3">$1</h3>')
      .replace(/^## (.*$)/gim, '<h2 class="theme-markdown-h2">$1</h2>')
      .replace(/^# (.*$)/gim, '<h1 class="theme-markdown-h1">$1</h1>')
      // Bold
      .replace(/\*\*(.*?)\*\*/g, '<strong class="theme-markdown-strong">$1</strong>')
      // Lists
      .replace(/^\* (.*$)/gim, '<li class="ml-4">$1</li>')
      .replace(/^- (.*$)/gim, '<li class="ml-4">$1</li>')
      // Line breaks
      .replace(/\n\n/g, '<br/><br/>')
      .replace(/\n/g, '<br/>');
  }
}
