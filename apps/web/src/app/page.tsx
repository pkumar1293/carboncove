import Link from 'next/link'
import { CBAM_SECTORS, PRODUCTION_ROUTES } from '@/lib/constants'
export default function HomePage() {
  return (
    <div className="flex flex-col">
      <header className="border-b bg-card/80 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
          <span className="text-xl font-bold text-primary">CarbonCove</span>
          <nav className="flex items-center gap-4 text-sm">
            <Link href="/calculator" className="text-muted-foreground hover:text-primary">
              Calculator
            </Link>
            <Link href="/login" className="text-muted-foreground hover:text-primary">
              Sign in
            </Link>
            <Link
              href="/calculator"
              className="inline-flex h-8 items-center rounded-lg bg-primary px-3 text-sm font-medium text-primary-foreground"
            >
              Free estimate
            </Link>
          </nav>
        </div>
      </header>

      <section className="bg-primary px-4 py-20 text-primary-foreground sm:px-6">
        <div className="mx-auto max-w-3xl text-center">
          <p className="mb-4 text-sm font-medium uppercase tracking-wide opacity-80">
            CBAM compliance for Indian exporters
          </p>
          <h1 className="text-4xl font-bold leading-tight sm:text-5xl">
            Stop paying ₹3 crore in unnecessary CBAM tax
          </h1>
          <p className="mx-auto mt-6 max-w-xl text-lg opacity-90">
            Calculate your actual embedded emissions vs EU defaults. Prove lower carbon
            intensity and cut your Carbon Border Adjustment Mechanism liability.
          </p>
          <div className="mt-10 flex flex-wrap justify-center gap-4">
            <Link
              href="/calculator"
              className="inline-flex h-10 items-center rounded-lg bg-secondary px-6 text-base font-semibold text-primary"
            >
              Free CBAM calculator
            </Link>
          </div>
        </div>
      </section>

      <section className="border-b bg-card py-12">
        <div className="mx-auto grid max-w-6xl grid-cols-2 gap-8 px-4 sm:grid-cols-4 sm:px-6">
          {[
            { v: '₹1.5–3.5 Cr', l: 'Typical overpayment vs actuals' },
            { v: '18%', l: "India's global CBAM share" },
            { v: '740+', l: 'Entities in scope' },
            { v: '€80/t', l: 'EU ETS reference price' },
          ].map((s) => (
            <div key={s.l} className="text-center">
              <p className="text-2xl font-bold text-primary">{s.v}</p>
              <p className="mt-1 text-sm text-muted-foreground">{s.l}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <h2 className="text-center text-2xl font-bold">How it works</h2>
        <div className="mt-10 grid gap-8 md:grid-cols-3">
          {[
            { n: '1', t: 'Enter plant data', d: 'Sector, fuel, electricity, EU export volume' },
            { n: '2', t: 'Calculate CBAM', d: 'Scope 1 + 2 per EU Reg 2023/1773' },
            { n: '3', t: 'Save & report', d: 'Track compliance and generate declarations' },
          ].map((step) => (
            <div key={step.n} className="rounded-xl border bg-card p-6 text-center">
              <span className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-primary text-lg font-bold text-primary-foreground">
                {step.n}
              </span>
              <h3 className="mt-4 font-semibold">{step.t}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{step.d}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-muted/50 px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-6xl">
          <h2 className="text-center text-2xl font-bold">CBAM sectors we cover</h2>
          <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {CBAM_SECTORS.map((sector) => {
              const route = PRODUCTION_ROUTES[sector.value]?.[0]
              return (
                <div key={sector.value} className="rounded-xl border bg-card p-5">
                  <span className="text-2xl">{sector.icon}</span>
                  <h3 className="mt-2 font-semibold">{sector.label}</h3>
                  {route && (
                    <p className="mt-1 text-xs text-muted-foreground">
                      Typical: {route.typical_intensity} tCO₂/t ({route.label})
                    </p>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      </section>


      <footer className="mt-auto border-t bg-card px-4 py-8 text-center text-sm text-muted-foreground">
        <div className="flex flex-wrap justify-center gap-6">
          <Link href="/calculator">Calculator</Link>
          <Link href="/login">Login</Link>
          <Link href="/signup">Sign up</Link>
        </div>
        <p className="mt-4">© {new Date().getFullYear()} CarbonCove · EU Reg 2023/1773 compliant</p>
      </footer>
    </div>
  )
}
