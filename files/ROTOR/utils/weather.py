import json
import numpy as np

import numpy as np
from scipy.interpolate import CubicSpline

with open('grid_lat_lon_data.json') as f:
    grid_nos,lats,lons = json.load(f)

with open('grid_data.json') as f:
    grid_data = json.load(f)



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
    ((g_no1, dist),(g_no2, dist)) = get_two_nearest_grid_ids(lat_lon['lat'],lat_lon['lon'])
    
    data_temp_avg = grid_data[g_no1]['TEMPERATURE_AVG']
    

    # Original monthly means
    monthly_means = np.array(data_temp_avg)

    # Mid-month days
    days_of_month = np.array([15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349])

    # Extend data to include day 380 = Jan again for periodicity
    extended_days = np.append(days_of_month, 380)
    extended_means = np.append(monthly_means, monthly_means[0])

    # Fit periodic spline
    spline = CubicSpline(extended_days, extended_means, bc_type='periodic')

    # Interpolate daily values
    days = np.arange(1, 366)
    daily_temps = spline(days)

