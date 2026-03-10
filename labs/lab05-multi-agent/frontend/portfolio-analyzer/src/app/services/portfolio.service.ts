import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { PortfolioInput } from '../models/portfolio.model';
import { AnalysisResponse } from '../models/analysis.model';

@Injectable({
  providedIn: 'root'
})
export class PortfolioService {
  private readonly apiUrl = 'https://ai-training-ob17.onrender.com';

  constructor(private http: HttpClient) {}

  analyzePortfolio(portfolio: PortfolioInput): Observable<AnalysisResponse> {
    return this.http.post<AnalysisResponse>(
      `${this.apiUrl}/analyze`,
      portfolio
    ).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An error occurred while analyzing your portfolio.';
    
    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Backend error
      errorMessage = error.error?.detail || 
                     `Server error: ${error.status} ${error.statusText}`;
    }
    
    return throwError(() => new Error(errorMessage));
  }
}
