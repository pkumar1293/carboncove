'use client'

import { createContext, useContext, useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { api } from '@/lib/api'
import type { Company, Installation, User } from '@/lib/types'

interface AppContextValue {
  user: User | null
  company: Company | null
  installations: Installation[]
  activeInstallation: Installation | null
  setActiveInstallation: (i: Installation) => void
  loading: boolean
  refreshCompany: () => Promise<void>
}

const AppContext = createContext<AppContextValue>({
  user: null,
  company: null,
  installations: [],
  activeInstallation: null,
  setActiveInstallation: () => {},
  loading: true,
  refreshCompany: async () => {},
})

export function AppProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [company, setCompany] = useState<Company | null>(null)
  const [installations, setInstallations] = useState<Installation[]>([])
  const [activeInstallation, setActiveInstallation] = useState<Installation | null>(null)
  const [loading, setLoading] = useState(true)
  const supabase = createClient()

  useEffect(() => {
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange(async (_event, session) => {
      if (session?.access_token) {
        api.defaults.headers.common.Authorization = `Bearer ${session.access_token}`
        await loadUserData()
      } else {
        setUser(null)
        setCompany(null)
        setInstallations([])
        delete api.defaults.headers.common.Authorization
      }
      setLoading(false)
    })
    return () => subscription.unsubscribe()
  }, [])

  async function loadUserData() {
    try {
      const [userResp, instResp] = await Promise.all([
        api.get('/users/me'),
        api.get('/installations'),
      ])
      setUser(userResp.data.user)
      setCompany(userResp.data.company)
      const list = instResp.data.installations as Installation[]
      setInstallations(list)
      if (list.length > 0) setActiveInstallation(list[0])
    } catch {
      /* API unavailable or user not provisioned */
    }
  }

  async function refreshCompany() {
    const resp = await api.get('/users/me')
    setCompany(resp.data.company)
  }

  return (
    <AppContext.Provider
      value={{
        user,
        company,
        installations,
        activeInstallation,
        setActiveInstallation,
        loading,
        refreshCompany,
      }}
    >
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)
