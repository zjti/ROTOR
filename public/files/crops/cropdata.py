from dataclasses import dataclass
from typing import Optional

@dataclass
class HarvestProduct:
    """Represents a single harvest product (e.g., Korn, Stroh, Blatt)."""
    name: str
    dry_matter_percent: Optional[float] = None  # TM in %
    nitrogen_kg_per_dt: Optional[float] = None  # N (kg/dt FM)
    phosphate_oxide_kg_per_dt: Optional[float] = None  # P2O5 (kg/dt FM)
    potassium_oxide_kg_per_dt: Optional[float] = None  # K2O (kg/dt FM)
    magnesium_oxide_kg_per_dt: Optional[float] = None  # MgO (kg/dt FM)
    crude_protein_percent: Optional[float] = None  # Rohprotein (%)

@dataclass
class CropData:
    """Main dataclass for crop data, including straw and combined values."""
    crop_code: str
    real_name: str
    table_name: str
    crop_group: str
    primary_product: HarvestProduct
    straw_product: Optional[HarvestProduct] = None
    combined_nitrogen: Optional[float] = None  # N (Korn + Stroh)
    combined_phosphate: Optional[float] = None  # P2O5 (Korn + Stroh)
    combined_potassium: Optional[float] = None  # K2O (Korn + Stroh)
    combined_magnesium: Optional[float] = None  # MgO (Korn + Stroh)
    yield_dt_per_ha: Optional[float] = None  # Ertrag (dt/ha FM)
    n_fix_kg_per_dt: Optional[float] = None  # N-Fix (kg/ha)
    hnv_ratio: Optional[float] = None  # HNV (1:x ratio)


ACK_BOHNE = CropData(
    crop_code="ACK_BOHNE",
    real_name="Ackerbohne",
    table_name="Ackerbohnen",
    crop_group="Körnerleguminosen",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=4.10,
        phosphate_oxide_kg_per_dt=1.20,
        potassium_oxide_kg_per_dt=1.40,
        magnesium_oxide_kg_per_dt=0.20,
        crude_protein_percent=29.8,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=1.50,
        phosphate_oxide_kg_per_dt=0.30,
        potassium_oxide_kg_per_dt=2.60,
        magnesium_oxide_kg_per_dt=0.30,
    ),
    combined_nitrogen=5.60,
    combined_phosphate=1.50,
    combined_potassium=4.00,
    combined_magnesium=0.50,
    yield_dt_per_ha=35.0,
    n_fix_kg_per_dt=5.00,
    hnv_ratio=1.0,
)

DINKEL = CropData(
    crop_code="DINKEL",
    real_name="Dinkel",
    table_name="Dinkel (mit Spelzen)",
    crop_group="Getreide",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=1.65,
        phosphate_oxide_kg_per_dt=0.80,
        potassium_oxide_kg_per_dt=0.80,
        magnesium_oxide_kg_per_dt=0.20,
        crude_protein_percent=10.9,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=0.50,
        phosphate_oxide_kg_per_dt=0.30,
        potassium_oxide_kg_per_dt=1.40,
        magnesium_oxide_kg_per_dt=0.20,
    ),
    combined_nitrogen=2.05,
    combined_phosphate=1.04,
    combined_potassium=1.92,
    combined_magnesium=0.36,
    yield_dt_per_ha=60.0,
    hnv_ratio=0.8,
)

FTTR_ERBSE = CropData(
    crop_code="FTTR_ERBSE",
    real_name="Futtererbse",
    table_name="Erbsen",
    crop_group="Körnerleguminosen",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=3.60,
        phosphate_oxide_kg_per_dt=1.10,
        potassium_oxide_kg_per_dt=1.40,
        magnesium_oxide_kg_per_dt=0.20,
        crude_protein_percent=26.2,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=1.50,
        phosphate_oxide_kg_per_dt=0.30,
        potassium_oxide_kg_per_dt=2.60,
        magnesium_oxide_kg_per_dt=0.30,
    ),
    yield_dt_per_ha=35.0,
    n_fix_kg_per_dt=4.40,
)

FTTR_RUEBE = CropData(
    crop_code="FTTR_RUEBE",
    real_name="Futterrübe",
    table_name="Futterrüben, Runkelrüben (Gehaltsrüben)",
    crop_group="Hackfrüchte",
    primary_product=HarvestProduct(
        name="Rübe",
        dry_matter_percent=15.0,
        nitrogen_kg_per_dt=0.18,
        phosphate_oxide_kg_per_dt=0.09,
        potassium_oxide_kg_per_dt=0.50,
        magnesium_oxide_kg_per_dt=0.05,
    ),
    straw_product=HarvestProduct(
        name="Blatt",
        dry_matter_percent=16.0,
        nitrogen_kg_per_dt=0.30,
        phosphate_oxide_kg_per_dt=0.08,
        potassium_oxide_kg_per_dt=0.63,
        magnesium_oxide_kg_per_dt=0.08,
    ),
    combined_nitrogen=0.30,
    combined_phosphate=0.12,
    combined_potassium=0.75,
    combined_magnesium=0.08,
    yield_dt_per_ha=650.0,
    hnv_ratio=0.4,
)

HAFER = CropData(
    crop_code="HAFER",
    real_name="Hafer",
    table_name="Sommerhafer",
    crop_group="Getreide",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=1.51,
        phosphate_oxide_kg_per_dt=0.80,
        potassium_oxide_kg_per_dt=0.60,
        magnesium_oxide_kg_per_dt=0.20,
        crude_protein_percent=11.0,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=0.50,
        phosphate_oxide_kg_per_dt=0.30,
        potassium_oxide_kg_per_dt=1.70,
        magnesium_oxide_kg_per_dt=0.20,
    ),
    combined_nitrogen=2.06,
    combined_phosphate=1.13,
    combined_potassium=2.47,
    combined_magnesium=0.42,
    yield_dt_per_ha=55.0,
    hnv_ratio=1.1,
)

KRN_MAIS = CropData(
    crop_code="KRN_MAIS",
    real_name="Körnermais",
    table_name="Körnermais, sonstige Körnernutzung",
    crop_group="Körnermais",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=1.38,
        phosphate_oxide_kg_per_dt=0.80,
        potassium_oxide_kg_per_dt=0.50,
        magnesium_oxide_kg_per_dt=0.20,
        crude_protein_percent=10.0,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=0.90,
        phosphate_oxide_kg_per_dt=0.20,
        potassium_oxide_kg_per_dt=2.00,
        magnesium_oxide_kg_per_dt=0.40,
    ),
    combined_nitrogen=2.28,
    combined_phosphate=1.00,
    combined_potassium=2.50,
    combined_magnesium=0.60,
    yield_dt_per_ha=90.0,
    hnv_ratio=1.0,
)

LEG_GRAS = CropData(
    crop_code="LEG_GRAS",
    real_name="Leguminosengras",
    table_name="Not listed",
    crop_group="Not listed",
    primary_product=HarvestProduct(name="Not listed"),
)

LUPINE = CropData(
    crop_code="LUPINE",
    real_name="Lupine",
    table_name="Lupinen blau",
    crop_group="Körnerleguminosen",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=4.48,
        phosphate_oxide_kg_per_dt=1.02,
        potassium_oxide_kg_per_dt=0.99,
        magnesium_oxide_kg_per_dt=0.20,
        crude_protein_percent=32.6,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=1.50,
        phosphate_oxide_kg_per_dt=0.30,
        potassium_oxide_kg_per_dt=2.60,
        magnesium_oxide_kg_per_dt=0.30,
    ),
    combined_nitrogen=5.98,
    combined_phosphate=1.32,
    combined_potassium=3.59,
    combined_magnesium=0.50,
    yield_dt_per_ha=30.0,
    n_fix_kg_per_dt=5.00,
    hnv_ratio=1.0,
)

SILO_MAIS = CropData(
    crop_code="SILO_MAIS",
    real_name="Silomais",
    table_name="Silomais (32 % TM)",
    crop_group="Futterpflanzen",
    primary_product=HarvestProduct(
        name="Ganzpflanze",
        dry_matter_percent=32.0,
        nitrogen_kg_per_dt=0.43,
        phosphate_oxide_kg_per_dt=0.16,
        potassium_oxide_kg_per_dt=0.51,
        magnesium_oxide_kg_per_dt=0.10,
    ),
    yield_dt_per_ha=450.0,
)

SOJA = CropData(
    crop_code="SOJA",
    real_name="Soja",
    table_name="Sojabohnen",
    crop_group="Körnerleguminosen",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=4.40,
        phosphate_oxide_kg_per_dt=1.50,
        potassium_oxide_kg_per_dt=1.70,
        magnesium_oxide_kg_per_dt=0.50,
        crude_protein_percent=32.0,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=1.50,
        phosphate_oxide_kg_per_dt=0.30,
        potassium_oxide_kg_per_dt=4.00,
        magnesium_oxide_kg_per_dt=1.20,
    ),
    combined_nitrogen=5.90,
    combined_phosphate=1.80,
    combined_potassium=5.70,
    combined_magnesium=1.70,
    yield_dt_per_ha=20.0,
    n_fix_kg_per_dt=5.3,
    hnv_ratio=1.0,
)

SM_WEIZEN = CropData(
    crop_code="SM_WEIZEN",
    real_name="Sommerweizen",
    table_name="Sommerweizen",
    crop_group="Getreide",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=2.11,
        phosphate_oxide_kg_per_dt=0.75,
        potassium_oxide_kg_per_dt=0.55,
        magnesium_oxide_kg_per_dt=0.20,
        crude_protein_percent=14.0,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=0.50,
        phosphate_oxide_kg_per_dt=0.30,
        potassium_oxide_kg_per_dt=1.40,
        magnesium_oxide_kg_per_dt=0.20,
    ),
    combined_nitrogen=2.51,
    combined_phosphate=0.99,
    combined_potassium=1.67,
    combined_magnesium=0.36,
    yield_dt_per_ha=70.0,
    hnv_ratio=0.8,
)

SM_GERST = CropData(
    crop_code="SM_GERST",
    real_name="Sommergerste",
    table_name="Sommerfuttergerste",
    crop_group="Getreide",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=1.65,
        phosphate_oxide_kg_per_dt=0.80,
        potassium_oxide_kg_per_dt=0.60,
        magnesium_oxide_kg_per_dt=0.20,
        crude_protein_percent=12.0,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=0.50,
        phosphate_oxide_kg_per_dt=0.30,
        potassium_oxide_kg_per_dt=1.70,
        magnesium_oxide_kg_per_dt=0.10,
    ),
    combined_nitrogen=2.05,
    combined_phosphate=1.04,
    combined_potassium=1.96,
    combined_magnesium=0.28,
    yield_dt_per_ha=50.0,
    hnv_ratio=0.8,
)

SP_KART = CropData(
    crop_code="SP_KART",
    real_name="Speisekartoffeln",
    table_name="Kartoffel (Speise, Stärke)",
    crop_group="Hackfrüchte",
    primary_product=HarvestProduct(
        name="Knolle",
        dry_matter_percent=22.0,
        nitrogen_kg_per_dt=0.35,
        phosphate_oxide_kg_per_dt=0.14,
        potassium_oxide_kg_per_dt=0.60,
        magnesium_oxide_kg_per_dt=0.04,
    ),
    straw_product=HarvestProduct(
        name="Kraut",
        dry_matter_percent=15.0,
        nitrogen_kg_per_dt=0.20,
        phosphate_oxide_kg_per_dt=0.04,
        potassium_oxide_kg_per_dt=0.36,
        magnesium_oxide_kg_per_dt=0.08,
    ),
    combined_nitrogen=0.39,
    combined_phosphate=0.15,
    combined_potassium=0.67,
    combined_magnesium=0.06,
    yield_dt_per_ha=450.0,
    hnv_ratio=0.2,
)

SP_MOEHR = CropData(
    crop_code="SP_MOEHR",
    real_name="Speisemöhren",
    table_name="Not listed",
    crop_group="Not listed",
    primary_product=HarvestProduct(name="Not listed"),
)

STECK_RUEBE = CropData(
    crop_code="STECK_RUEBE",
    real_name="Steckrüben",
    table_name="Kohl-, Steckrüben",
    crop_group="Hackfrüchte",
    primary_product=HarvestProduct(
        name="Rübe",
        dry_matter_percent=12.0,
        nitrogen_kg_per_dt=0.14,
        phosphate_oxide_kg_per_dt=0.07,
        potassium_oxide_kg_per_dt=0.45,
        magnesium_oxide_kg_per_dt=0.05,
    ),
    straw_product=HarvestProduct(
        name="Blatt",
        dry_matter_percent=16.0,
        nitrogen_kg_per_dt=0.25,
        phosphate_oxide_kg_per_dt=0.06,
        potassium_oxide_kg_per_dt=0.38,
        magnesium_oxide_kg_per_dt=0.08,
    ),
    combined_nitrogen=0.24,
    combined_phosphate=0.09,
    combined_potassium=0.60,
    combined_magnesium=0.08,
    yield_dt_per_ha=900.0,
    hnv_ratio=0.4,
)

TRITICALE = CropData(
    crop_code="TRITICALE",
    real_name="Triticale",
    table_name="Triticale",
    crop_group="Getreide",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=1.65,
        phosphate_oxide_kg_per_dt=0.80,
        potassium_oxide_kg_per_dt=0.60,
        magnesium_oxide_kg_per_dt=0.20,
        crude_protein_percent=12.0,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=0.50,
        phosphate_oxide_kg_per_dt=0.30,
        potassium_oxide_kg_per_dt=1.70,
        magnesium_oxide_kg_per_dt=0.20,
    ),
    combined_nitrogen=2.10,
    combined_phosphate=1.07,
    combined_potassium=2.13,
    combined_magnesium=0.38,
    yield_dt_per_ha=70.0,
    hnv_ratio=0.9,
)

WN_GERSTE = CropData(
    crop_code="WN_GERSTE",
    real_name="Wintergerste",
    table_name="Wintergerste",
    crop_group="Getreide",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=1.65,
        phosphate_oxide_kg_per_dt=0.80,
        potassium_oxide_kg_per_dt=0.60,
        magnesium_oxide_kg_per_dt=0.20,
        crude_protein_percent=12.0,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=0.50,
        phosphate_oxide_kg_per_dt=0.30,
        potassium_oxide_kg_per_dt=1.70,
        magnesium_oxide_kg_per_dt=0.10,
    ),
    combined_nitrogen=2.00,
    combined_phosphate=1.01,
    combined_potassium=1.79,
    combined_magnesium=0.27,
    yield_dt_per_ha=70.0,
    hnv_ratio=0.7,
)

WN_RAPS = CropData(
    crop_code="WN_RAPS",
    real_name="Winterraps",
    table_name="Winterraps",
    crop_group="Ölfrüchte",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=91.0,
        nitrogen_kg_per_dt=3.35,
        phosphate_oxide_kg_per_dt=1.80,
        potassium_oxide_kg_per_dt=1.00,
        magnesium_oxide_kg_per_dt=0.50,
        crude_protein_percent=23.0,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=0.70,
        phosphate_oxide_kg_per_dt=0.40,
        potassium_oxide_kg_per_dt=2.35,
        magnesium_oxide_kg_per_dt=0.41,
    ),
    combined_nitrogen=4.54,
    combined_phosphate=2.48,
    combined_potassium=5.00,
    combined_magnesium=1.20,
    yield_dt_per_ha=40.0,
    hnv_ratio=1.7,
)

WN_ROGGEN = CropData(
    crop_code="WN_ROGGEN",
    real_name="Winterroggen",
    table_name="Winterroggen",
    crop_group="Getreide",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=1.86,
        phosphate_oxide_kg_per_dt=1.01,
        potassium_oxide_kg_per_dt=1.79,
        magnesium_oxide_kg_per_dt=0.27,
        crude_protein_percent=11.0,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=0.50,
        phosphate_oxide_kg_per_dt=0.30,
        potassium_oxide_kg_per_dt=2.00,
        magnesium_oxide_kg_per_dt=0.20,
    ),
    combined_nitrogen=1.96,
    combined_phosphate=1.07,
    combined_potassium=2.40,
    combined_magnesium=0.28,
    yield_dt_per_ha=70.0,
    hnv_ratio=0.9,
)

WN_WEIZEN = CropData(
    crop_code="WN_WEIZEN",
    real_name="Winterweizen",
    table_name="Winterweizen C-Sorte",
    crop_group="Getreide",
    primary_product=HarvestProduct(
        name="Korn",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=1.81,
        phosphate_oxide_kg_per_dt=0.80,
        potassium_oxide_kg_per_dt=0.55,
        magnesium_oxide_kg_per_dt=0.20,
        crude_protein_percent=12.0,
    ),
    straw_product=HarvestProduct(
        name="Stroh",
        dry_matter_percent=86.0,
        nitrogen_kg_per_dt=0.50,
        phosphate_oxide_kg_per_dt=0.30,
        potassium_oxide_kg_per_dt=1.40,
        magnesium_oxide_kg_per_dt=0.20,
    ),
    combined_nitrogen=2.21,
    combined_phosphate=1.04,
    combined_potassium=1.67,
    combined_magnesium=0.36,
    yield_dt_per_ha=80.0,
    hnv_ratio=0.8,
)

ZUCKER_RUEBE = CropData(
    crop_code="ZUCKER_RUEBE",
    real_name="Zuckerrübe",
    table_name="Zuckerrüben",
    crop_group="Hackfrüchte",
    primary_product=HarvestProduct(
        name="Rübe",
        dry_matter_percent=23.0,
        nitrogen_kg_per_dt=0.18,
        phosphate_oxide_kg_per_dt=0.10,
        potassium_oxide_kg_per_dt=0.25,
        magnesium_oxide_kg_per_dt=0.08,
    ),
    straw_product=HarvestProduct(
        name="Blatt",
        dry_matter_percent=18.0,
        nitrogen_kg_per_dt=0.40,
        phosphate_oxide_kg_per_dt=0.11,
        potassium_oxide_kg_per_dt=0.71,
        magnesium_oxide_kg_per_dt=0.10,
    ),
    combined_nitrogen=0.46,
    combined_phosphate=0.18,
    combined_potassium=0.75,
    combined_magnesium=0.15,
    yield_dt_per_ha=650.0,
    hnv_ratio=0.7,
)

ZWIBELN = CropData(
    crop_code="ZWIBELN",
    real_name="Zwiebeln",
    table_name="Not listed",
    crop_group="Not listed",
    primary_product=HarvestProduct(name="Not listed"),
)
 