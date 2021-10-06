"""Module containing main logic to create sequence of trips."""
from datetime import datetime, timedelta
from typing import List

import numpy as np
import pandas as pd

from utils import append_trip


def create_synthetic_data(known_locations: List[dict],
                          travel_time_dict: dict,
                          location_scatter: bool,
                          departure_time_scatter: bool,
                          travel_time_scatter: bool,
                          monthly_trip: bool,
                          seasonal_trip: bool,
                          additional_holidays=None,
                          start_date: datetime = datetime(year=2018, month=1, day=1),
                          end_date: datetime = datetime(year=2019, month=12, day=31)) -> pd.DataFrame:
    """Main logic to create sequence of trips given the passed parameters.

    Args:
        known_locations:        List of JSON representing locations
        travel_time_dict:       Matrix (as JSON) for travel times in between locations
        location_scatter:       Flag to indicate if location scatter should be applied
        departure_time_scatter: Flag to indicate if departure time scatter should be applied
        travel_time_scatter:    Flag to indicate if travel time scatter should be applied
        monthly_trip:           Flag to indicate if monthly trips should be included
        seasonal_trip:          Flag to indicate if seasonal trips should be included
        additional_holidays:    Optional list of holidays, e.g. from user's calendar etc.
        start_date:             First day of relevant time range
        end_date:               Last day of relevant time range

    Returns:
        Dataframe containing sequence of trips, one trip per row.
        Columns:
            "gps_start_lat":    Latitude of GPS position at start of trip
            "gps_start_lon":    Longitude of GPS position at start of trip
            "t_start":          Start time of trip as UTC time code in Milliseconds
            "t_end":            End time of trip as UTC time code in Milliseconds
            "gps_end_lat":      Latitude of GPS position at end of trip
            "gps_end_lon":      Longitude of GPS position at end of trip
    """
    if additional_holidays is None:
        additional_holidays = []

    # initialize dataframe
    df_trips = pd.DataFrame(columns=["gps_start_lat",
                                     "gps_start_lon",
                                     "t_start",
                                     "t_end",
                                     "gps_end_lat",
                                     "gps_end_lon"])

    # initialize flag to indicate if monthly trip has been taken
    monthly_trip_taken = False

    # loop over each day in given time range
    for day in [start_date + timedelta(days=d) for d in range((end_date - start_date).days)]:

        if day.month != (day - timedelta(days=1)).month:
            # reset monthly trip flag
            monthly_trip_taken = False

        if day.weekday() == 0 and day not in additional_holidays:  # Monday
            # take monthly trip on first Monday of month
            if not monthly_trip_taken and monthly_trip:
                df_trips = append_trip(start_location='home',
                                       start_time=day.replace(hour=8, minute=0),
                                       end_location='back_office',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict
                                       )

                df_trips = append_trip(start_location='back_office',
                                       start_time=day.replace(hour=15, minute=45),
                                       end_location='home',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)

                # set monthly trip flag
                monthly_trip_taken = True
            else:
                df_trips = append_trip(start_location='home',
                                       start_time=day.replace(hour=6, minute=0),
                                       end_location='work',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)

                df_trips = append_trip(start_location='work',
                                       start_time=day.replace(hour=16, minute=30),
                                       end_location='home',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)

        if day.weekday() == 1 and day not in additional_holidays:  # Tuesday
            df_trips = append_trip(start_location='home',
                                   start_time=day.replace(hour=6, minute=0),
                                   end_location='work',
                                   df=df_trips,
                                   location_scatter=location_scatter,
                                   departure_time_scatter=departure_time_scatter,
                                   travel_time_scatter=travel_time_scatter,
                                   known_locations=known_locations,
                                   travel_time_dict=travel_time_dict)

            if seasonal_trip and day.month in [5, 6, 7, 8, 9]:
                df_trips = append_trip(start_location='work',
                                       start_time=day.replace(hour=14, minute=45),
                                       end_location='swimming',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict
                                       )
                df_trips = append_trip(start_location='swimming',
                                       start_time=day.replace(hour=16, minute=20),
                                       end_location='home',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict
                                       )
            else:
                df_trips = append_trip(start_location='work',
                                       start_time=day.replace(hour=16, minute=30),
                                       end_location='home',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)

        if day.weekday() == 2 and day not in additional_holidays:  # Wednesday
            df_trips = append_trip(start_location='home',
                                   start_time=day.replace(hour=6, minute=0),
                                   end_location='work',
                                   df=df_trips,
                                   location_scatter=location_scatter,
                                   departure_time_scatter=departure_time_scatter,
                                   travel_time_scatter=travel_time_scatter,
                                   known_locations=known_locations,
                                   travel_time_dict=travel_time_dict)
            if int(np.random.randint(2)) == 1:
                df_trips = append_trip(start_location='work',
                                       start_time=day.replace(hour=16, minute=30),
                                       end_location='grocery',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)

                df_trips = append_trip(start_location='grocery',
                                       start_time=day.replace(hour=17, minute=15),
                                       end_location='home',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)
            else:

                df_trips = append_trip(start_location='work',
                                       start_time=day.replace(hour=16, minute=30),
                                       end_location='home',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)

            df_trips = append_trip(start_location='home',
                                   start_time=day.replace(hour=18, minute=24),
                                   end_location='workout',
                                   df=df_trips,
                                   location_scatter=location_scatter,
                                   departure_time_scatter=departure_time_scatter,
                                   travel_time_scatter=travel_time_scatter,
                                   known_locations=known_locations,
                                   travel_time_dict=travel_time_dict)

            df_trips = append_trip(start_location='workout',
                                   start_time=day.replace(hour=20, minute=49),
                                   end_location='home',
                                   df=df_trips,
                                   location_scatter=location_scatter,
                                   departure_time_scatter=departure_time_scatter,
                                   travel_time_scatter=travel_time_scatter,
                                   known_locations=known_locations,
                                   travel_time_dict=travel_time_dict)

        if day.weekday() == 3 and day not in additional_holidays:  # Thursday
            df_trips = append_trip(start_location='home',
                                   start_time=day.replace(hour=6, minute=15),
                                   end_location='work',
                                   df=df_trips,
                                   location_scatter=location_scatter,
                                   departure_time_scatter=departure_time_scatter,
                                   travel_time_scatter=travel_time_scatter,
                                   known_locations=known_locations,
                                   travel_time_dict=travel_time_dict)

            if seasonal_trip and day.month in [5, 6, 7, 8, 9]:
                df_trips = append_trip(start_location='work',
                                       start_time=day.replace(hour=15, minute=20),
                                       end_location='swimming',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)
                df_trips = append_trip(start_location='swimming',
                                       start_time=day.replace(hour=17, minute=0),
                                       end_location='home',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)
            else:
                df_trips = append_trip(start_location='work',
                                       start_time=day.replace(hour=16, minute=30),
                                       end_location='home',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)

        if day.weekday() == 4 and day not in additional_holidays:  # Friday
            df_trips = append_trip(start_location='home',
                                   start_time=day.replace(hour=6, minute=0),
                                   end_location='work',
                                   df=df_trips,
                                   location_scatter=location_scatter,
                                   departure_time_scatter=departure_time_scatter,
                                   travel_time_scatter=travel_time_scatter,
                                   known_locations=known_locations,
                                   travel_time_dict=travel_time_dict)

            if int(np.random.randint(2)) == 1:
                df_trips = append_trip(start_location='work',
                                       start_time=day.replace(hour=15, minute=30),
                                       end_location='grocery',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)

                df_trips = append_trip(start_location='grocery',
                                       start_time=day.replace(hour=16, minute=15),
                                       end_location='home',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)
            else:

                df_trips = append_trip(start_location='work',
                                       start_time=day.replace(hour=15, minute=30),
                                       end_location='home',
                                       df=df_trips,
                                       location_scatter=location_scatter,
                                       departure_time_scatter=departure_time_scatter,
                                       travel_time_scatter=travel_time_scatter,
                                       known_locations=known_locations,
                                       travel_time_dict=travel_time_dict)

            df_trips = append_trip(start_location='home',
                                   start_time=day.replace(hour=19, minute=27),
                                   end_location='orchestra',
                                   df=df_trips,
                                   location_scatter=location_scatter,
                                   departure_time_scatter=departure_time_scatter,
                                   travel_time_scatter=travel_time_scatter,
                                   known_locations=known_locations,
                                   travel_time_dict=travel_time_dict)

            df_trips = append_trip(start_location='orchestra',
                                   start_time=day.replace(hour=22, minute=15),
                                   end_location='home',
                                   df=df_trips,
                                   location_scatter=location_scatter,
                                   departure_time_scatter=departure_time_scatter,
                                   travel_time_scatter=travel_time_scatter,
                                   known_locations=known_locations,
                                   travel_time_dict=travel_time_dict)

        if day.weekday() == 5:  # Saturday
            df_trips = append_trip(start_location='home',
                                   start_time=day.replace(hour=10, minute=0),
                                   end_location='grocery',
                                   df=df_trips,
                                   location_scatter=location_scatter,
                                   departure_time_scatter=departure_time_scatter,
                                   travel_time_scatter=travel_time_scatter,
                                   known_locations=known_locations,
                                   travel_time_dict=travel_time_dict)

            df_trips = append_trip(start_location='grocery',
                                   start_time=day.replace(hour=11, minute=5),
                                   end_location='home',
                                   df=df_trips,
                                   location_scatter=location_scatter,
                                   departure_time_scatter=departure_time_scatter,
                                   travel_time_scatter=travel_time_scatter,
                                   known_locations=known_locations,
                                   travel_time_dict=travel_time_dict)

        if day.weekday() == 6:  # Sunday
            df_trips = append_trip(start_location='home',
                                   start_time=day.replace(hour=11, minute=55),
                                   end_location='parents',
                                   df=df_trips,
                                   location_scatter=location_scatter,
                                   departure_time_scatter=departure_time_scatter,
                                   travel_time_scatter=travel_time_scatter,
                                   known_locations=known_locations,
                                   travel_time_dict=travel_time_dict)

            df_trips = append_trip(start_location='parents',
                                   start_time=day.replace(hour=15, minute=0),
                                   end_location='home',
                                   df=df_trips,
                                   location_scatter=location_scatter,
                                   departure_time_scatter=departure_time_scatter,
                                   travel_time_scatter=travel_time_scatter,
                                   known_locations=known_locations,
                                   travel_time_dict=travel_time_dict)

    return df_trips
