export function formatINR(value: number): string {
  const absVal = Math.abs(value)
  const formatted = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(absVal)
  return value < 0 ? `-${formatted}` : formatted
}

export function formatTonne(value: number, decimals = 2): string {
  return `${value.toLocaleString('en-IN', { maximumFractionDigits: decimals })} t`
}

export function formatCO2(value: number, decimals = 3): string {
  return `${value.toLocaleString('en-IN', { maximumFractionDigits: decimals })} tCO₂`
}

export function formatCO2Intensity(value: number): string {
  return `${value.toFixed(4)} tCO₂/t`
}
