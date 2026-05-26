'use client'

import { CBAM_SECTORS } from '@/lib/constants'

export function SectorSelector({
  value,
  onChange,
}: {
  value: string
  onChange: (sector: string) => void
}) {
  return (
    <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
      {CBAM_SECTORS.map((sector) => (
        <button
          key={sector.value}
          type="button"
          onClick={() => onChange(sector.value)}
          className={`rounded-xl border-2 p-4 text-left transition-all ${
            value === sector.value
              ? 'border-primary bg-green-50 text-primary'
              : 'border-border text-foreground hover:border-primary/40'
          }`}
        >
          <div className="mb-1 text-2xl">{sector.icon}</div>
          <div className="text-sm font-medium">{sector.label}</div>
        </button>
      ))}
    </div>
  )
}
