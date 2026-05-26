'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import {
  LayoutDashboard,
  Factory,
  ClipboardList,
  Calculator,
  FileText,
  Settings,
  LogOut,
} from 'lucide-react'
import { createClient } from '@/lib/supabase/client'
import { useApp } from '@/contexts/AppContext'

const NAV = [
  { href: '/app/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/app/installations', label: 'Installations', icon: Factory },
  { href: '/app/data-entry', label: 'Data Entry', icon: ClipboardList },
  { href: '/app/calculate', label: 'Calculate', icon: Calculator },
  { href: '/app/reports', label: 'Reports', icon: FileText },
  { href: '/app/settings', label: 'Settings', icon: Settings },
]

export function Sidebar() {
  const pathname = usePathname()
  const router = useRouter()
  const { user, company } = useApp()

  async function logout() {
    const supabase = createClient()
    await supabase.auth.signOut()
    router.push('/login')
  }

  return (
    <aside className="sticky top-0 flex h-screen w-60 shrink-0 flex-col border-r bg-card">
      <div className="border-b px-6 py-5">
        <span className="text-xl font-bold text-primary">CarbonCove</span>
        {company?.subscription_tier && company.subscription_tier !== 'free' && (
          <span className="ml-2 rounded-full bg-accent px-2 py-0.5 text-xs capitalize text-accent-foreground">
            {company.subscription_tier}
          </span>
        )}
      </div>
      <nav className="flex-1 space-y-1 overflow-y-auto px-3 py-4">
        {NAV.map(({ href, label, icon: Icon }) => {
          const active = pathname.startsWith(href)
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                active
                  ? 'bg-green-50 text-primary'
                  : 'text-muted-foreground hover:bg-muted hover:text-foreground'
              }`}
            >
              <Icon size={18} />
              {label}
            </Link>
          )
        })}
      </nav>
      <div className="border-t px-4 py-4">
        {company?.subscription_tier === 'free' && (
          <Link
            href="/app/upgrade"
            className="mb-3 block rounded-lg bg-primary py-2 text-center text-xs font-semibold text-primary-foreground"
          >
            Upgrade plan
          </Link>
        )}
        <div className="flex items-center gap-2 text-sm">
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-100 text-xs font-bold text-primary">
            {user?.full_name?.[0]?.toUpperCase() || 'U'}
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate font-medium">{user?.full_name || 'User'}</p>
            <p className="truncate text-xs text-muted-foreground">{company?.name}</p>
          </div>
          <button type="button" onClick={logout} title="Log out">
            <LogOut size={16} className="text-muted-foreground" />
          </button>
        </div>
      </div>
    </aside>
  )
}
