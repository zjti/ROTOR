import json
import numpy as np
from datetime import datetime, timedelta

import numpy as np
from scipy.interpolate import CubicSpline

with open('grid_lat_lon_data.json') as f:
    grid_nos,lats,lons = json.load(f)

with open('grid_data.json') as f:
    grid_data = json.load(f)

daily_weather = {}

def day_index_to_mmdd(day_index, year=2021):
    """
    Convert a 0-based day-of-year index to a 'MMDD' string.
    
    Parameters:
        day_index : int  - day of year index (0 = Jan 1)
        year      : int  - year for leap-year handling (default: 2021)
    
    Returns:
        str - MMDD formatted string
    """
    base_date = datetime(year, 1, 1)
    target_date = base_date + timedelta(days=day_index)
    return target_date.strftime("%m%d")


def day_index_to_month(day_index, year=2021):
    """
    Convert a 0-based day-of-year index to the corresponding month (1–12).
    
    Parameters:
        day_index : int    - 0-based day of year (0 = Jan 1)
        year      : int    - year to resolve leap years (default: 2021)
        
    Returns:
        int - Month number (1–12)
    """
    base_date = datetime(year, 1, 1)
    target_date = base_date + timedelta(days=day_index)
    return target_date.month


def mmdd_to_day_index(mmdd_str):
    """
    Convert a 'MMDD' string to day-of-year index (0-based).
    
    Example:
        '0101' → 0
        '1231' → 364 (or 365 in leap years)
    """
    dt = datetime.strptime(mmdd_str, '%m%d')
    return dt.timetuple().tm_yday - 1  # zero-based

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
    


def load_from_lat_lon(lat_lon):

    """
     ['TEMPERATURE_MAX', 'TEMPERATURE_MIN', 'TEMPERATURE_AVG',
                 'PRECIPITATION', 'ET0', 'RADIATION']
    """
    global daily_weather
    
    ((g_no1, dist),(g_no2, dist)) = get_two_nearest_grid_ids(lat_lon['lat'],lat_lon['lon'])

    days = np.arange(1, 366)
    # Mid-month days
    days_of_month = np.array([15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349])

    for KEY in ['TEMPERATURE_MAX', 'TEMPERATURE_MIN', 'TEMPERATURE_AVG','PRECIPITATION', 'ET0', 'RADIATION']:
        monthly_means = np.array(grid_data[str(g_no1)][KEY])
    
        # Extend data to include day 380 = Jan again for periodicity
        extended_days = np.append(days_of_month, 380)
        extended_means = np.append(monthly_means, monthly_means[0])
        # Fit periodic spline
        spline = CubicSpline(extended_days, extended_means, bc_type='periodic')
    
        daily_weather[ KEY ] = spline(days)

     


