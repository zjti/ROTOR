import json

with open('grid_lat_lon_data.json') as f:
    grid_nos,lats,lons = json.load(f)

with open('grid_data.json') as f:
    grid_data = json.load(f)


import numpy as np

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
    Return the grid_nos of the 2 nearest locations to a given lat/lon.
    
    Parameters:
        lat, lon      : float - target coordinates
        grid_nos      : np.array - array of grid IDs
        lats, lons    : np.array - coordinates for each grid ID
        
    Returns:
        tuple of (nearest_id, second_nearest_id)
    """
    dists = haversine(lat, lon, lats, lons)
    nearest_idxs = np.argsort(dists)[:2]
    return grid_nos[nearest_idxs[0]], grid_nos[nearest_idxs[1]]

# get_two_nearest_grid_ids(12,8,grid_nos, lats,lons)