export interface User {
  id: string
  company_id: string
  full_name: string
  role: 'owner' | 'admin' | 'member' | 'viewer'
  created_at: string
}

export interface Company {
  id: string
  name: string
  gstin?: string
  pan?: string
  address?: string
  city?: string
  state?: string
  pin_code?: string
  contact_name?: string
  contact_email: string
  contact_phone?: string
  subscription_tier: 'free' | 'starter' | 'professional' | 'business' | 'enterprise'
  subscription_valid_until?: string
  razorpay_subscription_id?: string
  created_at: string
  updated_at: string
}

export interface Installation {
  id: string
  company_id: string
  name: string
  sector: 'iron_steel' | 'aluminium' | 'cement' | 'fertiliser' | 'hydrogen' | 'electricity'
  production_route: string
  state: string
  grid_region: 'Northern' | 'Southern' | 'Eastern' | 'Western' | 'North-Eastern' | 'Andaman' | 'default'
  has_captive_power: boolean
  captive_power_type?: string
  annual_capacity_tonnes?: number
  address?: string
  created_at: string
}

export interface Product {
  id: string
  installation_id: string
  cn_code: string
  hs_code: string
  product_name: string
  production_route_detail?: Record<string, unknown>
  is_active: boolean
  created_at: string
}

export interface ActivityData {
  id: string
  installation_id: string
  product_id?: string
  reporting_period_start: string
  reporting_period_end: string
  data_type: string
  fuel_type?: string
  quantity: number
  unit: string
  source?: string
  notes?: string
  created_by?: string
  created_at: string
}

export interface EmissionResult {
  id: string
  installation_id: string
  product_id?: string
  reporting_period_start: string
  reporting_period_end: string
  scope1_direct: number
  scope2_indirect: number
  total_embedded: number
  production_volume: number
  specific_embedded: number
  eu_default_value: number
  savings_vs_default: number
  eu_ets_price_used: number
  eur_to_inr_rate: number
  cbam_cost_actual: number
  cbam_cost_default: number
  calculation_version: string
  input_data?: Record<string, unknown>
  created_at: string
}

export interface Report {
  id: string
  company_id: string
  installation_id?: string
  report_type: string
  reporting_year: number
  status: 'draft' | 'generating' | 'ready' | 'error'
  file_url?: string
  generated_at?: string
  created_at: string
}

export interface Subscription {
  tier: 'free' | 'starter' | 'professional' | 'business' | 'enterprise'
  valid_until?: string
  razorpay_subscription_id?: string
}

export interface Lead {
  id: string
  email: string
  company_name?: string
  sector?: string
  annual_export_tonnes?: number
  estimated_cbam_cost?: number
  utm_source?: string
  created_at: string
}

export interface QuickEstimateResponse {
  specific_embedded_tco2_per_tonne: number
  eu_default_tco2_per_tonne: number
  total_scope1_tco2: number
  total_scope2_tco2: number
  cbam_cost_actual_eur: number
  cbam_cost_actual_inr: number
  cbam_cost_default_eur: number
  cbam_cost_default_inr: number
  savings_eur: number
  savings_inr: number
  export_tonnes: number
  eu_ets_price_eur: number
}
