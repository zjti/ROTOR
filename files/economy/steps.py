from dataclasses import dataclass

@dataclass
class WorkSettings:
    distance_km = 8
    size_ha = 3

@dataclass
class WorkStep:
    work_settings = WorkSettings()
    name = ''
    date = 'JAN01'
        
@dataclass
class SeedingStep(WorkStep):
    pass

@dataclass
class HarvestStep(WorkStep):
    pass

@dataclass
class MainProductHarvestStep(HarvestStep):
    pass

@dataclass
class ByProductHarvestStep(HarvestStep):
    pass

@dataclass
class FertilzerStep(WorkStep):
    pass

@dataclass
class SolidFertilizerStep(FertilzerStep):
    pass

@dataclass
class LiquidFertilizerStep(FertilzerStep):
    pass

@dataclass
class SoilManagementStep(WorkStep):
    pass

