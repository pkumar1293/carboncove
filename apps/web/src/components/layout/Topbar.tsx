'use client'

import { usePathname } from 'next/navigation'

const PAGE_TITLES: Record<string, string> = {
  '/app/dashboard': 'Dashboard',
  '/app/installations': 'Installations',
  '/app/data-entry': 'Data Entry',
  '/app/calculate': 'Calculate',
  '/app/reports': 'Reports',
  '/app/settings': 'Settings',
  '/app/upgrade': 'Upgrade Plan',
}

export function Topbar() {
  const pathname = usePathname()
  const title =
    Object.entries(PAGE_TITLES).find(([key]) => pathname.startsWith(key))?.[1] ||
    'CarbonCove'

  return (
    <header className="sticky top-0 z-10 flex h-14 items-center border-b bg-card px-6">
      <h1 className="text-lg font-semibold">{title}</h1>
    </header>
  )
}
