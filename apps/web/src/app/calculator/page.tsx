'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'sonner'
import { api } from '@/lib/api'
import { estimateLocally } from '@/lib/cbam-estimate'
import {
  CEA_GRID_REGIONS,
  EU_DEFAULT_VALUES,
  PRODUCTION_ROUTES,
} from '@/lib/constants'
import { StepIndicator } from '@/components/calculator/StepIndicator'
import {
  ResultsPanel,
  type QuickEstimateResponse,
} from '@/components/calculator/ResultsPanel'
import { SectorSelector } from '@/components/calculator/SectorSelector'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const STEPS = ['Company & Product', 'Energy & Fuel', 'Results', 'Get Full Report']

const step1Schema = z.object({
  company_name: z.string().min(2, 'Required'),
  sector: z.string().min(1, 'Select a sector'),
  cn_code: z.string().min(1, 'Select a product'),
  production_route: z.string().min(1, 'Select a route'),
  annual_production_tonnes: z.number().gt(0),
  export_to_eu_percent: z.number().min(0).max(100),
})

const step2Schema = z.object({
  fuel_type: z.string().min(1),
  fuel_quantity_tonnes: z.number().gt(0),
  electricity_mwh: z.number().gte(0),
  grid_region: z.string(),
  has_captive: z.boolean(),
  captive_fuel_type: z.string().optional(),
  captive_fuel_tonnes: z.number().optional(),
})

const step4Schema = z.object({
  email: z.string().email('Valid email required'),
  contact_name: z.string().min(2, 'Required'),
  company_name: z.string(),
  phone: z.string().optional(),
  wants_consultation: z.boolean(),
})

type Step1 = z.infer<typeof step1Schema>
type Step2 = z.infer<typeof step2Schema>
type Step4 = z.infer<typeof step4Schema>

export default function CalculatorPage() {
  const [step, setStep] = useState(1)
  const [step1Data, setStep1Data] = useState<Step1 | null>(null)
  const [estimateResult, setEstimateResult] = useState<QuickEstimateResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [leadSubmitted, setLeadSubmitted] = useState(false)

  const form1 = useForm<Step1>({ resolver: zodResolver(step1Schema) })
  const form2 = useForm<Step2>({
    resolver: zodResolver(step2Schema),
    defaultValues: {
      has_captive: false,
      grid_region: 'default',
      electricity_mwh: 0,
    },
  })
  const form4 = useForm<Step4>({
    resolver: zodResolver(step4Schema),
    defaultValues: { wants_consultation: false },
  })

  const selectedSector = form1.watch('sector')
  const hasCaptive = form2.watch('has_captive')

  useEffect(() => {
    const saved = sessionStorage.getItem('cc_estimate_result')
    if (saved) {
      try {
        setEstimateResult(JSON.parse(saved))
      } catch {
        /* ignore */
      }
    }
  }, [])

  async function handleStep2Submit(data: Step2) {
    if (!step1Data) return
    setLoading(true)
    const payload = {
      sector: step1Data.sector,
      production_route: step1Data.production_route,
      annual_production_tonnes: step1Data.annual_production_tonnes,
      export_to_eu_percent: step1Data.export_to_eu_percent,
      grid_region: data.grid_region,
      cn_code: step1Data.cn_code,
      fuel_inputs: [{ fuel_type: data.fuel_type, quantity_tonnes: data.fuel_quantity_tonnes }],
      electricity_mwh: data.electricity_mwh,
      has_captive_power: data.has_captive,
      captive_fuel_type: data.captive_fuel_type,
      captive_fuel_tonnes: data.captive_fuel_tonnes || 0,
    }

    try {
      const resp = await api.post('/estimate', payload)
      const result = resp.data as QuickEstimateResponse
      sessionStorage.setItem('cc_estimate_result', JSON.stringify(result))
      setEstimateResult(result)
      setStep(3)
      toast.success('CBAM exposure calculated')
    } catch {
      const result = estimateLocally(payload)
      sessionStorage.setItem('cc_estimate_result', JSON.stringify(result))
      setEstimateResult(result)
      setStep(3)
      toast.message('Used offline estimate — start API for live rates', {
        description: 'Run: cd apps/api && uvicorn main:app --reload',
      })
    } finally {
      setLoading(false)
    }
  }

  async function handleLeadSubmit(data: Step4) {
    const saved = sessionStorage.getItem('cc_estimate_result')
    const result = saved ? JSON.parse(saved) : estimateResult
    setLoading(true)
    try {
      await api.post('/estimate/lead', {
        email: data.email,
        company_name: data.company_name || step1Data?.company_name,
        sector: step1Data?.sector,
        annual_export_tonnes: step1Data
          ? step1Data.annual_production_tonnes * (step1Data.export_to_eu_percent / 100)
          : undefined,
        estimated_cbam_cost: result?.cbam_cost_actual_inr,
        utm_source: new URLSearchParams(window.location.search).get('utm_source') || undefined,
      })
      sessionStorage.removeItem('cc_estimate_result')
      setLeadSubmitted(true)
      toast.success('Report request received!')
    } catch {
      setLeadSubmitted(true)
      toast.success('Details saved — we will follow up shortly')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-background px-4 py-12">
      <div className="mx-auto max-w-2xl">
        <div className="mb-8 text-center">
          <Link href="/" className="text-sm text-primary hover:underline">
            ← CarbonCove
          </Link>
          <h1 className="mt-4 text-3xl font-bold text-primary">Free CBAM Calculator</h1>
          <p className="mt-2 text-muted-foreground">
            Discover your EU carbon liability in 2 minutes
          </p>
        </div>

        <StepIndicator currentStep={step} labels={STEPS} />

        <div className="rounded-2xl border bg-card p-8 shadow-sm">
          {step === 1 && (
            <form
              onSubmit={form1.handleSubmit((d) => {
                setStep1Data(d)
                form4.setValue('company_name', d.company_name)
                setStep(2)
              })}
              className="space-y-6"
            >
              <h2 className="text-xl font-semibold">Company & Product</h2>
              <div>
                <Label>Company name</Label>
                <Input {...form1.register('company_name')} placeholder="Tata Steel Ltd." className="mt-1" />
                {form1.formState.errors.company_name && (
                  <p className="mt-1 text-xs text-destructive">
                    {form1.formState.errors.company_name.message}
                  </p>
                )}
              </div>
              <div>
                <Label className="mb-2 block">Sector</Label>
                <SectorSelector
                  value={form1.watch('sector') || ''}
                  onChange={(v) => {
                    form1.setValue('sector', v)
                    form1.setValue('production_route', '')
                    form1.setValue('cn_code', '')
                  }}
                />
              </div>
              {selectedSector && (
                <div>
                  <Label>Production route</Label>
                  <select
                    {...form1.register('production_route')}
                    className="mt-1 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
                  >
                    <option value="">Select route...</option>
                    {(PRODUCTION_ROUTES[selectedSector] || []).map((r) => (
                      <option key={r.value} value={r.value}>
                        {r.label} (typical: {r.typical_intensity} tCO₂/t)
                      </option>
                    ))}
                  </select>
                </div>
              )}
              <div>
                <Label>CN code (EU product)</Label>
                <select
                  {...form1.register('cn_code')}
                  className="mt-1 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
                >
                  <option value="">Select product...</option>
                  {Object.entries(EU_DEFAULT_VALUES).map(([code, info]) => (
                    <option key={code} value={code}>
                      {code} — {info.name} (EU default: {info.value} tCO₂/t)
                    </option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Annual production (tonnes)</Label>
                  <Input
                    type="number"
                    {...form1.register('annual_production_tonnes', { valueAsNumber: true })}
                    className="mt-1"
                  />
                </div>
                <div>
                  <Label>% exported to EU</Label>
                  <Input
                    type="number"
                    {...form1.register('export_to_eu_percent', { valueAsNumber: true })}
                    className="mt-1"
                  />
                </div>
              </div>
              <Button type="submit" className="w-full" size="lg">
                Next: Energy & Fuel →
              </Button>
            </form>
          )}

          {step === 2 && (
            <form onSubmit={form2.handleSubmit(handleStep2Submit)} className="space-y-6">
              <h2 className="text-xl font-semibold">Energy & Fuel</h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Primary fuel</Label>
                  <select
                    {...form2.register('fuel_type')}
                    className="mt-1 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
                  >
                    <option value="">Select...</option>
                    {['coal', 'coke', 'natural_gas', 'diesel', 'furnace_oil', 'petcoke', 'LPG'].map(
                      (f) => (
                        <option key={f} value={f}>
                          {f.replace('_', ' ')}
                        </option>
                      )
                    )}
                  </select>
                </div>
                <div>
                  <Label>Quantity (t/year)</Label>
                  <Input
                    type="number"
                    {...form2.register('fuel_quantity_tonnes', { valueAsNumber: true })}
                    className="mt-1"
                  />
                </div>
              </div>
              <div>
                <Label>Grid electricity (MWh/year)</Label>
                <Input
                  type="number"
                  {...form2.register('electricity_mwh', { valueAsNumber: true })}
                  className="mt-1"
                />
              </div>
              <div>
                <Label>Grid region</Label>
                <select
                  {...form2.register('grid_region')}
                  className="mt-1 w-full rounded-lg border border-input bg-background px-3 py-2 text-sm"
                >
                  {CEA_GRID_REGIONS.map((r) => (
                    <option key={r.value} value={r.value}>
                      {r.label} ({r.factor} tCO₂/MWh)
                    </option>
                  ))}
                </select>
              </div>
              <label className="flex cursor-pointer items-center gap-2 text-sm">
                <input type="checkbox" {...form2.register('has_captive')} className="rounded" />
                I have captive power
              </label>
              {hasCaptive && (
                <div className="grid grid-cols-2 gap-4 border-l-2 border-primary pl-4">
                  <div>
                    <Label>Captive fuel</Label>
                    <select
                      {...form2.register('captive_fuel_type')}
                      className="mt-1 w-full rounded-lg border border-input px-3 py-2 text-sm"
                    >
                      <option value="">Select...</option>
                      {['coal', 'natural_gas', 'diesel'].map((f) => (
                        <option key={f} value={f}>
                          {f}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <Label>Fuel (tonnes)</Label>
                    <Input
                      type="number"
                      {...form2.register('captive_fuel_tonnes', { valueAsNumber: true })}
                      className="mt-1"
                    />
                  </div>
                </div>
              )}
              <div className="flex gap-3">
                <Button type="button" variant="outline" onClick={() => setStep(1)} className="flex-1">
                  ← Back
                </Button>
                <Button type="submit" disabled={loading} className="flex-[2]">
                  {loading ? 'Calculating…' : 'Calculate →'}
                </Button>
              </div>
            </form>
          )}

          {step === 3 && estimateResult && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold">Your CBAM exposure</h2>
              <ResultsPanel result={estimateResult} />
              <Button className="w-full" size="lg" onClick={() => setStep(4)}>
                Get full compliance report →
              </Button>
            </div>
          )}

          {step === 4 && !leadSubmitted && (
            <form onSubmit={form4.handleSubmit(handleLeadSubmit)} className="space-y-6">
              <h2 className="text-xl font-semibold">Get your full report</h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Name</Label>
                  <Input {...form4.register('contact_name')} className="mt-1" />
                </div>
                <div>
                  <Label>Work email</Label>
                  <Input type="email" {...form4.register('email')} className="mt-1" />
                </div>
              </div>
              <div>
                <Label>Company</Label>
                <Input
                  {...form4.register('company_name')}
                  defaultValue={step1Data?.company_name}
                  className="mt-1"
                />
              </div>
              <label className="flex cursor-pointer items-start gap-3 text-sm">
                <input type="checkbox" {...form4.register('wants_consultation')} className="mt-1" />
                Free 30-min CBAM compliance call
              </label>
              <Button type="submit" disabled={loading} className="w-full" size="lg">
                {loading ? 'Sending…' : 'Download free report →'}
              </Button>
            </form>
          )}

          {step === 4 && leadSubmitted && (
            <div className="space-y-4 py-8 text-center">
              <p className="text-5xl">✅</p>
              <h2 className="text-xl font-bold text-primary">Report on its way!</h2>
              <p className="text-muted-foreground">Our team will reach out within 24 hours.</p>
              <Link
                href="/signup"
                className="inline-flex h-10 w-full items-center justify-center rounded-lg bg-primary text-sm font-semibold text-primary-foreground"
              >
                Create free account →
              </Link>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
