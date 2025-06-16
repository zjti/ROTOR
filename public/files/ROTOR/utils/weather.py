import json
import numpy as np
from scipy.interpolate import CubicSpline

from ROTOR.utils import config
from ROTOR.utils.modelvalue import ClassWithModelValues, UserEditableModelValue,ModelValue

with open('grid_lat_lon_data.json') as f:
    grid_nos,lats,lons = json.load(f)

with open('grid_data.json') as f:
    grid_data = json.load(f)

daily_weather = {}
monthly_weather = {}
monthly_weather_obj = {}


class MonthlyWeather(ClassWithModelValues):
    def __init__(self, key, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.key = key
        
        UserEditableModelValue('get_1',self.get_1)
        UserEditableModelValue('get_2',self.get_2)
        UserEditableModelValue('get_3',self.get_3)
        UserEditableModelValue('get_4',self.get_4)
        UserEditableModelValue('get_5',self.get_5)
        UserEditableModelValue('get_6',self.get_6)
        UserEditableModelValue('get_7',self.get_7)
        UserEditableModelValue('get_8',self.get_8)
        UserEditableModelValue('get_9',self.get_9)
        UserEditableModelValue('get_10',self.get_10)
        UserEditableModelValue('get_11',self.get_11)
        UserEditableModelValue('get_12',self.get_12)
        
        ModelValue('daily',self.daily)
        ModelValue('monthly',self.monthly)
        pass
    
    def monthly(self):
        return json.dumps([ self.get_monthly_mean(i) for i in range(1,13)])
    
    def daily(self):
        w = DailyWeather(self.key)
        return json.dumps( list(w.daily_weather.ravel()))
    
    def get_monthly_mean(self,month):
        if hasattr(self, f'get_{month}'):
            return getattr(self, f'get_{month}').__call__()
        return 0
    
    def get_1(self):
        return monthly_weather[self.key][0]
    def get_2(self):
        return monthly_weather[self.key][1]
    def get_3(self):
        return monthly_weather[self.key][2]
    def get_4(self):
        return monthly_weather[self.key][3]
    def get_5(self):
        return monthly_weather[self.key][4]
    def get_6(self):
        return monthly_weather[self.key][5]
    def get_7(self):
        return monthly_weather[self.key][6]
    def get_8(self):
        return monthly_weather[self.key][7]
    def get_9(self):
        return monthly_weather[self.key][8]
    def get_10(self):
        return monthly_weather[self.key][9]
    def get_11(self):
        return monthly_weather[self.key][10]
    def get_12(self):
        return monthly_weather[self.key][11]

for KEY in ['TEMPERATURE_MAX', 'TEMPERATURE_MIN', 'TEMPERATURE_AVG','PRECIPITATION', 'ET0', 'RADIATION']:
    monthly_weather_obj[KEY] = MonthlyWeather(KEY) #monthly_means
    

def haversine(lat1, lon1, lat2, lon2):
    """Compute haversine distance between two arrays of points (in degrees)."""
    R = 6371.0  # Earth radius in km
    lat1, lon1 = np.radians(lat1), np.radians(lon1)
    lat2, lon2 = np.radians(lat2), np.radians(lon2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    return 2 * R * np.arcsin(np.sqrt(a))

def get_two_nearest_grid_ids(lat, lon):
    """
    Return the two nearest grid_nos and their distances (in km) to a given lat/lon.
    
    Parameters:
        lat, lon   : float       - target location
        grid_nos   : np.ndarray  - array of GRID_NO values
        lats, lons : np.ndarray  - arrays of lat/lon for each grid point
        
    Returns:
        Tuple of: (grid_no_1, dist_1), (grid_no_2, dist_2)
    """
    dists = haversine(lat, lon, lats, lons)
    nearest_idxs = np.argsort(dists)[:2]
    
    return ((grid_nos[nearest_idxs[0]], dists[nearest_idxs[0]]),
            (grid_nos[nearest_idxs[1]], dists[nearest_idxs[1]]))
    
    
class DailyWeather:
    
    def __init__(self, KEY):
        monthly_weather = monthly_weather_obj[KEY]
        
        days = np.arange(1, 366)
        # Mid-month days
        days_of_month = np.array([15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349])
        monthly_means = np.array([monthly_weather.get_monthly_mean(i) for i in range(1,13)])

        # Extend data to include day 380 = Jan again for periodicity
        extended_days = np.append(days_of_month, 380)
        extended_means = np.append(monthly_means, monthly_means[0])
        # Fit periodic spline
        spline = CubicSpline(extended_days, extended_means, bc_type='periodic')
    
        self.daily_weather = spline(days)
        
    def get_day(self, day):
        return self.daily_weather[day]
    


def load_from_lat_lon(lat_lon):

    """
     ['TEMPERATURE_MAX', 'TEMPERATURE_MIN', 'TEMPERATURE_AVG',
                 'PRECIPITATION', 'ET0', 'RADIATION']
    """
    global daily_weather,monthly_weather,monthly_weather_obj
    
    ((g_no1, dist),(g_no2, dist)) = get_two_nearest_grid_ids(lat_lon['lat'],lat_lon['lon'])

    
    for KEY in ['TEMPERATURE_MAX', 'TEMPERATURE_MIN', 'TEMPERATURE_AVG','PRECIPITATION', 'ET0', 'RADIATION']:
        monthly_means = np.array(grid_data[str(g_no1)][KEY])
        
        monthly_weather [KEY] = monthly_means
        # monthly_weather_obj[KEY] = MonthlyWeather(KEY) #monthly_means
        
        daily_weather[KEY] = DailyWeather(KEY)

        # config.pyFolge.weather = monthly_weather_obj[KEY] 

