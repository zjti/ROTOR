from ROTOR.crop import Crop
from ROTOR.grainlegum import SummerGrainLegum
from ROTOR.crops.data import cropdata
from ROTOR.utils import config
from ROTOR.utils.js.jsmodel import VisFields as VF

from ROTOR.utils.modelvalue import ModelValue,UserEditableModelValue
from ROTOR.management.workstep import FertilizerStep, PrimaryTilageStep, ReducedPrimaryTilageStep, StriegelStep         

from ROTOR.utils import weather


class SOJA(SummerGrainLegum):

    price_yield_eur_per_dt_fm = 75.00
    seed_cost_eur_per_kg = 3.5
    seed_kg_per_ha = 120
    
    def __init__(self, *args, **kwargs):
        super().__init__(cropdata.SOJA, *args, **kwargs)

        self.hack_step = StriegelStep(name='Hacken', crop=self, date = 'APR2',
                                                 machine_cost_eur_per_ha=7.7,
                                                 diesel_l_per_ha= 4,
                                                 man_hours_h_per_ha= 0.55)
        
        
    
    def supports_undersowing(self):
        return False
    
    def get_crop_opts(self):
        return ["ZW_VOR","US_NACH","US_VOR"]
    
    def calc_yield_dt_fm_per_ha(self) -> float:
        """
        Calculate crop yield based on various parameters including:
        - Soil type
        - BKR (Bodenklimazahl-Region)
        - Ackerzahl (soil quality index)
        - Weather data
        
        Args:
            bkr: Integer representing the BKR region (101-147)
            soil_type: String representing soil type (e.g., "SOIL_L")
            ackerzahl: Float representing soil quality index
            weather_data: Dictionary containing monthly weather data with structure:
                {
                    month_index: {
                        "TEMPERATURE_AVG": float,
                        "PRECIPITATION": float
                    },
                    ...
                }
                where month_index 5=May, 6=June, etc.
        
        Returns:
            Calculated yield value
        """
        ackerzahl = config.SOIL['ACKERZAHL']['default']
        bkr = config.SOIL['BKR']['default']
        soil_type = config.SOIL['SOIL_TYPE']['default']
        # Initialize base yield
        yield_value = 12.6252498204505
        
        # Apply BKR corrections
        bkr_corrections = {
            101: -12.2529186719403,
            104: -9.53564783285671,
            107: -3.33349237703523,
            108: 8.73712526829197,
            109: 3.6144107677795,
            113: 1.36689656464902,
            114: -1.75123039957746,
            115: 6.2160672775463,
            116: 5.34065475646472,
            121: 2.65060814414095,
            122: 9.58182439928761,
            123: 3.53569166413136,
            132: -4.5385863912321,
            133: 3.65133198059314,
            141: -1.26172814134231,
            142: -2.74237240576269,
            146: -6.01468252063578,
            147: -3.26395208250203
        }
        if bkr in bkr_corrections:
            yield_value += bkr_corrections[bkr]
        
        # Apply soil type corrections
        soil_corrections = {
            "SOIL_L": -6.35963607193431,
            "SOIL_lS": 2.74168609885174,
            "SOIL_lU": 2.55025273798603,
            "SOIL_S": 1.76629414460148,
            "SOIL_sL": 0.202789232091692,
            "SOIL_sU": 0.555922309722489,
            "SOIL_T": -2.65511622263766,
            "SOIL_tL": 1.61401096274835,
            "SOIL_uL": -2.84226299227827,
            "SOIL_utL": 2.42605980084846
        }
        if soil_type in soil_corrections:
            yield_value += soil_corrections[soil_type]
        
        # Apply ackerzahl correction
        yield_value += 0.126540848535426 * ackerzahl
        
        try:    
            # Calculate weather metrics
            W = weather.monthly_weather_obj
            # Temperature calculations
            mean_temp_VE = (W["TEMPERATURE_AVG"].get_monthly_mean(5) + W["TEMPERATURE_AVG"].get_monthly_mean(6)) / 2
            mean_temp_BL = W["TEMPERATURE_AVG"].get_monthly_mean(7)
            mean_temp_PF = (W["TEMPERATURE_AVG"].get_monthly_mean(8) + W["TEMPERATURE_AVG"].get_monthly_mean(9)) / 2
            mean_temp_GS = sum(W["TEMPERATURE_AVG"].get_monthly_mean(m) for m in [5, 6, 7,8, 9]) / 5
            
            # Precipitation calculations (converted to monthly sums)
            sum_precipitation_VE = (W["PRECIPITATION"].get_monthly_mean(5) + W["PRECIPITATION"].get_monthly_mean(6)) / 2 * 30
            sum_precipitation_BL = W["PRECIPITATION"].get_monthly_mean(7) * 30
            sum_precipitation_PF = (W["PRECIPITATION"].get_monthly_mean(8) + W["PRECIPITATION"].get_monthly_mean(9)) / 2 * 30
            sum_precipitation_GS = sum(W["PRECIPITATION"].get_monthly_mean(m) for m in [5, 6, 7, 8, 9]) * 30
            
            # Apply weather corrections
            yield_value += -0.440908682626817 * mean_temp_BL
            yield_value += 0.852042367047337 * mean_temp_VE
            yield_value += -0.506621670762066 * mean_temp_PF
            yield_value += 0.484644818157224 * mean_temp_GS
            yield_value += 0.031692720024626 * sum_precipitation_GS
            yield_value += -0.018089703757958 * sum_precipitation_BL
            yield_value += -0.01519144520379 * sum_precipitation_VE
            yield_value += 0.0133513650708437 * sum_precipitation_PF
        except Exception as ex:
            print(ex)
            print(f"Missing required weather data for month:")
        
        return yield_value
            