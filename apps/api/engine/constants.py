"""CBAM calculation constants — EU Reg 2023/1773 compliant."""

EMISSION_FACTORS: dict[str, dict] = {
    "coal":        {"ncv": 26.7,  "ef": 0.0946, "unit": "tCO2/GJ"},
    "coke":        {"ncv": 28.2,  "ef": 0.1075, "unit": "tCO2/GJ"},
    "natural_gas": {"ncv": 44.4,  "ef": 0.0561, "unit": "tCO2/GJ"},
    "diesel":      {"ncv": 43.0,  "ef": 0.0741, "unit": "tCO2/GJ"},
    "furnace_oil": {"ncv": 40.4,  "ef": 0.0774, "unit": "tCO2/GJ"},
    "petcoke":     {"ncv": 32.5,  "ef": 0.0971, "unit": "tCO2/GJ"},
    "LPG":         {"ncv": 47.3,  "ef": 0.0632, "unit": "tCO2/GJ"},
}

CEA_GRID_FACTORS: dict[str, float] = {
    "Northern":      0.7078,   # tCO2/MWh — CEA 2023-24
    "Southern":      0.6987,
    "Eastern":       0.9196,
    "Western":       0.8038,
    "North-Eastern": 0.6023,
    "Andaman":       0.9100,
    "default":       0.7828,
}

EU_DEFAULT_VALUES: dict[str, dict] = {
    "7206.10": {"name": "Crude steel (BF-BOF)",             "value": 2.559},
    "7214.20": {"name": "TMT bars / rebar",                 "value": 2.171},
    "7208.10": {"name": "Hot rolled coil",                  "value": 2.275},
    "7601.10": {"name": "Unwrought aluminium (primary)",     "value": 6.070},
    "7601.20": {"name": "Secondary aluminium (unwrought)",   "value": 0.937},
    "7604.10": {"name": "Aluminium bars and rods",           "value": 6.256},
    "2523.10": {"name": "Cement clinker",                    "value": 0.812},
    "2523.29": {"name": "OPC cement",                        "value": 0.791},
    "3102.10": {"name": "Urea (fertiliser)",                 "value": 2.478},
    "2804.10": {"name": "Hydrogen",                          "value": 8.900},
}

OXIDATION_FACTOR = 1.0  # EU Reg 2023/1773 default

# Sector-specific process emission factors (per tonne of product)
PROCESS_EMISSION_FACTORS: dict[str, dict] = {
    "iron_steel": {
        "BF-BOF":    {"limestone_decomp_per_tonne": 0.065},
        "DRI-EAF":   {"limestone_decomp_per_tonne": 0.020},
        "EAF-scrap": {"limestone_decomp_per_tonne": 0.010},
    },
    "cement": {
        "dry-process": {"clinker_calcination_tco2_per_tonne_clinker": 0.525},
        "wet-process": {"clinker_calcination_tco2_per_tonne_clinker": 0.525},
    },
    "aluminium": {
        "primary-electrolysis": {"pfc_tco2_per_tonne_al": 1.65},  # pre-bake anode
        "secondary-recycled":   {"pfc_tco2_per_tonne_al": 0.0},
    },
}
