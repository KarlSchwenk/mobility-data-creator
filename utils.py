"""Module providing utility functions for creating synthetic mobility data."""
from datetime import datetime
from typing import List

import numpy as np
import pandas as pd


def travel_time(travel_time_dict: dict,
                start_location: str,
                end_location: str,
                travel_time_scatter: bool):
    if travel_time_scatter:
        tt_scatter = np.random.randn() * 0.05
    else:
        tt_scatter = 0.0

    # seconds
    return travel_time_dict[start_location][end_location] * (1 + tt_scatter)


def append_trip(known_locations: List[dict],
                travel_time_dict: dict,
                start_location: str,
                start_time: datetime,
                end_location: str,
                location_scatter: bool,
                departure_time_scatter: bool,
                travel_time_scatter: bool,
                df: pd.DataFrame) -> pd.DataFrame:
    if departure_time_scatter:
        # seconds
        if start_location == 'home':
            if start_time.hour < 12:
                dt_scatter = np.random.randn() * 5 * 60
            else:
                dt_scatter = np.random.randn() * 30 * 60
        elif start_location == 'work':
            dt_scatter = np.random.randn() * 45 * 60
        elif start_location == 'orchestra':
            dt_scatter = np.random.randn() * 5 * 60
        elif start_location == 'workout':
            dt_scatter = np.random.randn() * 10 * 60
        elif start_location == 'parents':
            dt_scatter = np.random.randn() * 60 * 60
        elif start_location == 'grocery':
            dt_scatter = np.random.randn() * 5 * 60
        elif start_location == 'swimming':
            dt_scatter = np.random.randn() * 20 * 60
        elif start_location == 'back_office':
            dt_scatter = np.random.randn() * 45 * 60
        else:
            dt_scatter = 0.0
    else:
        dt_scatter = 0.0

    if location_scatter:
        lat_scatter = np.random.randn() * 5e-4
        lon_scatter = np.random.randn() * 5e-4
    else:
        lat_scatter = 0.0
        lon_scatter = 0.0

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
    }, ignore_index=True)
