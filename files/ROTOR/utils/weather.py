import json
import numpy as np

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
    
     

# get_two_nearest_grid_ids(12,8,grid_nos, lats,lons)