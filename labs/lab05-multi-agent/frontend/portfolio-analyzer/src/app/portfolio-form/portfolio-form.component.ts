import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormArray, Validators, ReactiveFormsModule } from '@angular/forms';
import { PortfolioInput } from '../models/portfolio.model';

@Component({
  selector: 'app-portfolio-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './portfolio-form.component.html',
  styleUrl: './portfolio-form.component.css'
})
export class PortfolioFormComponent {
  @Output() submitPortfolio = new EventEmitter<PortfolioInput>();
  
  portfolioForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.portfolioForm = this.fb.group({
      client_id: [''],
      total_patrimony_brl: ['', [Validators.required, Validators.min(1)]],
      monthly_contribution_brl: [''],
      investment_horizon_months: [60, [Validators.min(1)]],
      current_assets: this.fb.array([])
    });

    // Add one empty asset by default
    this.addAsset();
  }

  get currentAssets(): FormArray {
    return this.portfolioForm.get('current_assets') as FormArray;
  }

  addAsset(): void {
    const assetGroup = this.fb.group({
      ticker: ['', Validators.required],
      quantity: ['', [Validators.required, Validators.min(0.01)]],
      current_price: ['', [Validators.required, Validators.min(0.01)]]
    });
    this.currentAssets.push(assetGroup);
  }

  removeAsset(index: number): void {
    if (this.currentAssets.length > 1) {
      this.currentAssets.removeAt(index);
    }
  }

  onSubmit(): void {
    if (this.portfolioForm.valid) {
      const formValue = this.portfolioForm.value;
      
      // Convert string values to numbers where needed
      const portfolio: PortfolioInput = {
        client_id: formValue.client_id || undefined,
        total_patrimony_brl: Number(formValue.total_patrimony_brl),
        monthly_contribution_brl: formValue.monthly_contribution_brl 
          ? Number(formValue.monthly_contribution_brl) 
          : undefined,
        investment_horizon_months: formValue.investment_horizon_months 
          ? Number(formValue.investment_horizon_months) 
          : 60,
        current_assets: formValue.current_assets.map((asset: any) => ({
          ticker: asset.ticker.toUpperCase(),
          quantity: Number(asset.quantity),
          current_price: Number(asset.current_price)
        }))
      };
      
      this.submitPortfolio.emit(portfolio);
    }
  }
}
