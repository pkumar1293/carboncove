'use client'

import { formatCO2Intensity, formatINR } from '@/lib/formatters'

export interface QuickEstimateResponse {
  specific_embedded_tco2_per_tonne: number
  eu_default_tco2_per_tonne: number
  cbam_cost_actual_inr: number
  cbam_cost_default_inr: number
  savings_inr: number
  export_to_eu_tonnes: number
  eu_ets_price_eur: number
}

export function ResultsPanel({ result }: { result: QuickEstimateResponse }) {
  const savingsPercent =
    result.cbam_cost_default_inr > 0
      ? ((result.savings_inr / result.cbam_cost_default_inr) * 100).toFixed(1)
      : '0'

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div className="rounded-lg border border-green-200 bg-green-50 p-4">
          <p className="mb-1 text-xs text-muted-foreground">Your actual intensity</p>
          <p className="text-2xl font-bold text-primary">
            {formatCO2Intensity(result.specific_embedded_tco2_per_tonne)}
          </p>
        </div>
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="mb-1 text-xs text-muted-foreground">EU default intensity</p>
          <p className="text-2xl font-bold text-red-600">
            {formatCO2Intensity(result.eu_default_tco2_per_tonne)}
          </p>
        </div>
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between rounded-lg border border-red-200 bg-red-50 p-4">
          <div>
            <p className="text-sm font-medium">CBAM using EU defaults</p>
            <p className="text-xs text-muted-foreground">Without actual emission data</p>
          </div>
          <p className="text-xl font-bold text-red-600">
            {formatINR(result.cbam_cost_default_inr)}
          </p>
        </div>
        <div className="flex items-center justify-between rounded-lg border border-green-200 bg-green-50 p-4">
          <div>
            <p className="text-sm font-medium">CBAM using actual data</p>
            <p className="text-xs text-muted-foreground">With verified plant data</p>
          </div>
          <p className="text-xl font-bold text-primary">
            {formatINR(result.cbam_cost_actual_inr)}
          </p>
        </div>
      </div>

      <div className="rounded-xl bg-primary p-6 text-center text-primary-foreground">
        <p className="mb-1 text-sm opacity-80">YOU SAVE</p>
        <p className="text-4xl font-extrabold">{formatINR(result.savings_inr)}</p>
        <p className="mt-1 text-sm opacity-80">
          {savingsPercent}% reduction in CBAM liability
        </p>
      </div>

      <p className="text-center text-xs text-muted-foreground">
        Based on EU ETS €{result.eu_ets_price_eur}/tCO₂ ·{' '}
        {result.export_to_eu_tonnes.toLocaleString('en-IN')} t EU export
      </p>
    </div>
  )
}
