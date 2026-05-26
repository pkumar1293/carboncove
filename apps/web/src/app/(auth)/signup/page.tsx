'use client'

import { useState } from 'react'
import Link from 'next/link'
import { createClient } from '@/lib/supabase/client'
import { toast } from 'sonner'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function SignupPage() {
  const [form, setForm] = useState({
    full_name: '',
    email: '',
    password: '',
    company_name: '',
  })
  const [loading, setLoading] = useState(false)
  const [verifyEmail, setVerifyEmail] = useState(false)

  async function handleSignup(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    const supabase = createClient()
    const { error } = await supabase.auth.signUp({
      email: form.email,
      password: form.password,
      options: {
        data: { full_name: form.full_name, company_name: form.company_name },
        emailRedirectTo: `${window.location.origin}/app/dashboard`,
      },
    })
    if (error) {
      toast.error(error.message)
      setLoading(false)
      return
    }
    setVerifyEmail(true)
  }

  if (verifyEmail) {
    return (
      <div className="rounded-2xl border bg-card p-8 text-center shadow-sm">
        <p className="text-5xl">📧</p>
        <h2 className="mt-4 text-xl font-bold">Check your email</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Verification link sent to <strong>{form.email}</strong>
        </p>
      </div>
    )
  }

  return (
    <div className="rounded-2xl border bg-card p-8 shadow-sm">
      <h2 className="mb-6 text-xl font-semibold">Create your account</h2>
      <form onSubmit={handleSignup} className="space-y-4">
        {(['full_name', 'company_name', 'email', 'password'] as const).map((field) => (
          <div key={field}>
            <Label className="capitalize">{field.replace('_', ' ')}</Label>
            <Input
              type={field === 'password' ? 'password' : field === 'email' ? 'email' : 'text'}
              value={form[field]}
              onChange={(e) => setForm({ ...form, [field]: e.target.value })}
              className="mt-1"
              required
            />
          </div>
        ))}
        <Button type="submit" disabled={loading} className="w-full">
          {loading ? 'Creating…' : 'Create free account'}
        </Button>
      </form>
      <p className="mt-4 text-center text-sm text-muted-foreground">
        Have an account?{' '}
        <Link href="/login" className="font-medium text-primary hover:underline">
          Sign in
        </Link>
      </p>
    </div>
  )
}
