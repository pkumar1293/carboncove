export const CBAM_SECTORS = [
  { value: 'iron_steel', label: 'Iron & Steel', icon: '🏗️' },
  { value: 'aluminium', label: 'Aluminium', icon: '🔩' },
  { value: 'cement', label: 'Cement', icon: '🏚️' },
  { value: 'fertiliser', label: 'Fertiliser', icon: '🌱' },
  { value: 'hydrogen', label: 'Hydrogen', icon: '⚡' },
  { value: 'electricity', label: 'Electricity', icon: '🔋' },
] as const

export const PRODUCTION_ROUTES: Record<string, { value: string; label: string; typical_intensity: number }[]> = {
  iron_steel: [
    { value: 'BF-BOF', label: 'Blast Furnace – Basic Oxygen Furnace', typical_intensity: 2.1 },
    { value: 'DRI-EAF', label: 'Direct Reduced Iron – Electric Arc Furnace', typical_intensity: 1.4 },
    { value: 'EAF-scrap', label: 'EAF (Scrap-based)', typical_intensity: 0.6 },
  ],
  aluminium: [
    { value: 'primary-electrolysis', label: 'Primary Electrolysis (Hall-Héroult)', typical_intensity: 6.1 },
    { value: 'secondary-recycled', label: 'Secondary (Recycled)', typical_intensity: 0.9 },
  ],
  cement: [
    { value: 'dry-process', label: 'Dry Process (Precalciner)', typical_intensity: 0.82 },
    { value: 'wet-process', label: 'Wet Process', typical_intensity: 1.05 },
  ],
  fertiliser: [
    { value: 'SMR-urea', label: 'Steam Methane Reforming – Urea', typical_intensity: 2.5 },
    { value: 'coal-gasification', label: 'Coal Gasification', typical_intensity: 3.8 },
  ],
  hydrogen: [
    { value: 'SMR', label: 'Steam Methane Reforming (Grey)', typical_intensity: 9.0 },
    { value: 'electrolysis-green', label: 'Electrolysis (Green)', typical_intensity: 0.5 },
  ],
  electricity: [
    { value: 'coal-thermal', label: 'Coal Thermal', typical_intensity: 0.95 },
    { value: 'gas-combined-cycle', label: 'Gas Combined Cycle', typical_intensity: 0.42 },
  ],
}

export const CEA_GRID_REGIONS = [
  { value: 'Northern', label: 'Northern Grid (Delhi, UP, Punjab…)', factor: 0.7078 },
  { value: 'Southern', label: 'Southern Grid (TN, Karnataka, AP…)', factor: 0.6987 },
  { value: 'Eastern', label: 'Eastern Grid (West Bengal, Odisha…)', factor: 0.9196 },
  { value: 'Western', label: 'Western Grid (Maharashtra, Gujarat…)', factor: 0.8038 },
  { value: 'North-Eastern', label: 'North-Eastern Grid', factor: 0.6023 },
  { value: 'Andaman', label: 'Andaman & Nicobar', factor: 0.9100 },
  { value: 'default', label: 'National Average', factor: 0.7828 },
]

export const EU_DEFAULT_VALUES: Record<string, { name: string; value: number }> = {
  '7206.10': { name: 'Crude steel (BF-BOF)', value: 2.559 },
  '7214.20': { name: 'TMT bars / rebar', value: 2.171 },
  '7208.10': { name: 'Hot rolled coil', value: 2.275 },
  '7601.10': { name: 'Unwrought aluminium (primary)', value: 6.070 },
  '7601.20': { name: 'Secondary aluminium (unwrought)', value: 0.937 },
  '7604.10': { name: 'Aluminium bars and rods', value: 6.256 },
  '2523.10': { name: 'Cement clinker', value: 0.812 },
  '2523.29': { name: 'OPC cement', value: 0.791 },
  '3102.10': { name: 'Urea (fertiliser)', value: 2.478 },
  '2804.10': { name: 'Hydrogen', value: 8.900 },
}

export const EU_ETS_PRICE_EUR_DEFAULT = 80
export const EUR_TO_INR_DEFAULT = 90
