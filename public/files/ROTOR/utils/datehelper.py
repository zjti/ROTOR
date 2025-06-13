from datetime import datetime, timedelta


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


def day_index_to_half_month(day_index, year=2021):
    """
    Convert a 0-based day-of-year index to a half-month string like 'JAN1', 'FEB2', etc.
    
    Parameters:
        day_index : int  - 0-based day of year (0 = Jan 1)
        year      : int  - year for leap-year handling (default: 2021)
    
    Returns:
        str - One of ['JAN1', 'JAN2', ..., 'DEZ2']
    """
    month_names = ['JAN', 'FEB', 'MRZ', 'APR', 'MAI', 'JUN',
                   'JUL', 'AUG', 'SEP', 'OKT', 'NOV', 'DEZ']
    
    base_date = datetime(year, 1, 1)
    target_date = base_date + timedelta(days=day_index)
    
    month_abbr = month_names[target_date.month - 1]
    half = '2' if target_date.day > 15 else '1'
    
    return f"{month_abbr}{half}"

