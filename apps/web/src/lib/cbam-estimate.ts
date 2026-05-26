/**
 * Client-side CBAM estimate fallback when API is unavailable (dev/demo).
 * Mirrors apps/api/engine logic at a high level.
 */
import {
  CEA_GRID_REGIONS,
  EU_DEFAULT_VALUES,
  EU_ETS_PRICE_EUR_DEFAULT,
  EUR_TO_INR_DEFAULT,
} from './constants'

const EMISSION_FACTORS: Record<string, { ncv: number; ef: number }> = {
  coal: { ncv: 26.7, ef: 0.0946 },
  coke: { ncv: 28.2, ef: 0.1075 },
  natural_gas: { ncv: 44.4, ef: 0.0561 },
  diesel: { ncv: 43.0, ef: 0.0741 },
  furnace_oil: { ncv: 40.4, ef: 0.0774 },
  petcoke: { ncv: 32.5, ef: 0.0971 },
  LPG: { ncv: 47.3, ef: 0.0632 },
}

const PROCESS: Record<string, Record<string, number>> = {
  iron_steel: { 'BF-BOF': 0.065, 'DRI-EAF': 0.02, 'EAF-scrap': 0.01 },
  cement: { 'dry-process': 0.525, 'wet-process': 0.525 },
  aluminium: { 'primary-electrolysis': 1.65, 'secondary-recycled': 0 },
}

export interface EstimatePayload {
  sector: string
  production_route: string
  annual_production_tonnes: number
  export_to_eu_percent: number
  grid_region: string
  cn_code: string
  fuel_inputs: { fuel_type: string; quantity_tonnes: number }[]
  electricity_mwh: number
  has_captive_power: boolean
  captive_fuel_type?: string
  captive_fuel_tonnes?: number
}

export interface QuickEstimateResult {
  specific_embedded_tco2_per_tonne: number
  eu_default_tco2_per_tonne: number
  cbam_cost_actual_inr: number
  cbam_cost_default_inr: number
  savings_inr: number
  export_to_eu_tonnes: number
  eu_ets_price_eur: number
}

function gridFactor(region: string): number {
  return CEA_GRID_REGIONS.find((r) => r.value === region)?.factor ?? 0.7828
}

export function estimateLocally(payload: EstimatePayload): QuickEstimateResult {
  let scope1 = 0
  for (const fi of payload.fuel_inputs) {
    const ef = EMISSION_FACTORS[fi.fuel_type]
    if (!ef) continue
    scope1 += fi.quantity_tonnes * ef.ncv * ef.ef
  }
  const proc =
    (PROCESS[payload.sector]?.[payload.production_route] ?? 0) *
    payload.annual_production_tonnes
  scope1 += proc

  let scope2 = payload.electricity_mwh * gridFactor(payload.grid_region)
  if (
    payload.has_captive_power &&
    payload.captive_fuel_type &&
    payload.captive_fuel_tonnes
  ) {
    const ef = EMISSION_FACTORS[payload.captive_fuel_type]
    if (ef) scope2 += payload.captive_fuel_tonnes * ef.ncv * ef.ef
  }

  const total = scope1 + scope2
  const production = payload.annual_production_tonnes
  const exportTonnes = production * (payload.export_to_eu_percent / 100)
  const specific = total / production
  const euDefault = EU_DEFAULT_VALUES[payload.cn_code]?.value ?? specific
  const ets = EU_ETS_PRICE_EUR_DEFAULT
  const eurInr = EUR_TO_INR_DEFAULT

  const cbamActualEur = specific * exportTonnes * ets
  const cbamDefaultEur = euDefault * exportTonnes * ets
  const savingsEur = cbamDefaultEur - cbamActualEur

  return {
    specific_embedded_tco2_per_tonne: Math.round(specific * 1e6) / 1e6,
    eu_default_tco2_per_tonne: euDefault,
    cbam_cost_actual_inr: Math.round(cbamActualEur * eurInr),
    cbam_cost_default_inr: Math.round(cbamDefaultEur * eurInr),
    savings_inr: Math.round(savingsEur * eurInr),
    export_to_eu_tonnes: exportTonnes,
    eu_ets_price_eur: ets,
  }
}
