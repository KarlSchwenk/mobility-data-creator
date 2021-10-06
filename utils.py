"""Module providing utility functions for creating synthetic mobility data."""
from datetime import datetime
from typing import List, Tuple

import numpy as np
import pandas as pd


def travel_time(travel_time_dict: dict,
                start_location: str,
                end_location: str,
                travel_time_scatter: bool) -> float:
    """Wrapper to fetch/calculate travel times with/without random scatter.

    Args:
        travel_time_dict:       Travel time matrix as dict
        start_location:         Name of start location
        end_location:           Name of end location
        travel_time_scatter:    Flag to indicate if travel time should be multiplied by random factor

    Returns:
        Travel time in seconds.
    """
    if travel_time_scatter:
        tt_scatter = np.random.randn() * 0.05
    else:
        tt_scatter = 0.0

    # seconds
    return travel_time_dict[start_location][end_location] * (1 + tt_scatter)


def _departure_time_scatter(start_location: str,
                            start_time: datetime) -> float:
    """Wrapper to simulate departure time scatter.

    Returns:
        Random float to offset departure time.
    """
    # seconds
    if start_location == 'home':
        if start_time.hour < 12:
            return np.random.randn() * 5 * 60
        else:
            return np.random.randn() * 30 * 60
    elif start_location == 'work':
        return np.random.randn() * 45 * 60
    elif start_location == 'orchestra':
        return np.random.randn() * 5 * 60
    elif start_location == 'workout':
        return np.random.randn() * 10 * 60
    elif start_location == 'parents':
        return np.random.randn() * 60 * 60
    elif start_location == 'grocery':
        return np.random.randn() * 5 * 60
    elif start_location == 'swimming':
        return np.random.randn() * 20 * 60
    elif start_location == 'back_office':
        return np.random.randn() * 45 * 60
    return 0.0


def _location_scatter() -> Tuple[float, float]:
    """Wrapper to simulate measurement scatter of GPS locations.

    Returns:
        Tuple of random scatter values.
    """
    return float(np.random.randn() * 5e-4), float(np.random.randn() * 5e-4)


def append_trip(known_locations: List[dict],
                travel_time_dict: dict,
                start_location: str,
                start_time: datetime,
                end_location: str,
                location_scatter: bool,
                departure_time_scatter: bool,
                travel_time_scatter: bool,
                df: pd.DataFrame) -> pd.DataFrame:
    """Utility to insert trip in Dataframe given the parameters passed.

    Args:
        known_locations:        List of JSON representing locations
        travel_time_dict:       Matrix (as JSON) for travel times in between locations
        start_location:         Name of trip start location
        start_time:             Start time of trip as datetime object
        end_location:           Name of trip end location
        location_scatter:       Flag to indicate if location scatter should be applied
        departure_time_scatter: Flag to indicate if departure time scatter should be applied
        travel_time_scatter:    Flag to indicate if travel time scatter should be applied
        df:                     Dataframe to append to

    Returns:
        Dataframe with appended trip as specified.
    """
    dt_scatter = _departure_time_scatter(start_location=start_location,
                                         start_time=start_time) if departure_time_scatter else 0.0

    lat_scatter, lon_scatter = _location_scatter() if location_scatter else (0.0, 0.0)

    return df.append({
        "gps_start_lat": [e["gps_lat"] for e in known_locations if e["name"] == start_location][0] + lat_scatter,
        "gps_start_lon": [e["gps_lon"] for e in known_locations if e["name"] == start_location][0] + lon_scatter,
        "t_start": (start_time.timestamp() + dt_scatter) * 1000,
        "t_end": (start_time.timestamp() + travel_time(start_location=start_location,
                                                       end_location=end_location,
                                                       travel_time_dict=travel_time_dict,
                                                       travel_time_scatter=travel_time_scatter) + dt_scatter) * 1000,
        "gps_end_lat": [e["gps_lat"] for e in known_locations if e["name"] == end_location][0] + lat_scatter,
        "gps_end_lon": [e["gps_lon"] for e in known_locations if e["name"] == end_location][0] + lon_scatter
    },
        ignore_index=True)
