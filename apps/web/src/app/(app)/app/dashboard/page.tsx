'use client'

import Link from 'next/link'
import { useApp } from '@/contexts/AppContext'
import { formatINR } from '@/lib/formatters'
import { Calculator, Factory, FileText } from 'lucide-react'

export default function DashboardPage() {
  const { company, installations } = useApp()

  return (
    <div className="mx-auto max-w-6xl space-y-6">
      <div>
        <h2 className="text-2xl font-semibold">
          Welcome{company?.name ? `, ${company.name}` : ''}
        </h2>
        <p className="mt-1 text-muted-foreground">Manage CBAM compliance for your EU exports.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <div className="rounded-xl border bg-card p-5">
          <p className="text-sm text-muted-foreground">Installations</p>
          <p className="text-3xl font-bold text-primary">{installations.length}</p>
        </div>
        <div className="rounded-xl border bg-card p-5">
          <p className="text-sm text-muted-foreground">Plan</p>
          <p className="text-3xl font-bold capitalize">{company?.subscription_tier || 'free'}</p>
        </div>
        <div className="rounded-xl border bg-primary p-5 text-primary-foreground">
          <p className="text-sm opacity-80">Potential savings</p>
          <p className="text-2xl font-bold">{formatINR(0)}</p>
          <p className="text-xs opacity-70">Run calculator to estimate</p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {[
          { href: '/app/data-entry', icon: Factory, label: 'Enter data', desc: 'Fuel & electricity' },
          { href: '/calculator', icon: Calculator, label: 'Quick estimate', desc: 'Public CBAM tool' },
          { href: '/app/reports', icon: FileText, label: 'Reports', desc: 'Agent F — coming next' },
        ].map((a) => (
          <Link
            key={a.href}
            href={a.href}
            className="rounded-xl border bg-card p-5 transition-shadow hover:shadow-md"
          >
            <a.icon className="text-primary" size={24} />
            <p className="mt-3 font-semibold">{a.label} →</p>
            <p className="text-xs text-muted-foreground">{a.desc}</p>
          </Link>
        ))}
      </div>

      {installations.length === 0 && (
        <div className="rounded-xl border border-dashed p-8 text-center">
          <p className="text-muted-foreground">No installations yet.</p>
          <Link
            href="/app/installations"
            className="mt-2 inline-block text-sm font-medium text-primary"
          >
            Add your first plant →
          </Link>
        </div>
      )}
    </div>
  )
}
