"""Main script to run creation of synthetic trip data."""
import json
from datetime import datetime, date
from trip_creation import create_synthetic_data
# --------------------------------------------------------------------------- #
# ADJUSTABLE PARAMETERS FOR CREATION OF SYNTHETIC DATA
# --------------------------------------------------------------------------- #
# JSON file containing list of known locations and their GPS locations
with open("data/known_locations.json", "r") as f:
    KNOWN_LOCATIONS = json.load(f)['data']

# JSON file containing travel time matrix in between known locations
with open("data/travel_times.json", "r") as f:
    TRAVEL_TIME = json.load(f)

# time range of data to create
START_DATE = datetime(year=2018, month=1, day=1)
END_DATE = datetime(year=2019, month=12, day=31)

# put scatter on GPS points
LOCATION_SCATTER = True

# put scatter on start time of trips
DEPARTURE_TIME_SCATTER = True

# put scatter on travel time of trips
TRAVEL_TIME_SCATTER = True

# go to back office once a month
MONTHLY_TRIP = True

# go to public swimming pool twice a week during summer
SEASONAL_TRIP = True

# list of additional holidays, e.g. from user calendar
ADDITIONAL_HOLIDAYS = [date(year=2018, month=1, day=d) for d in range(1, 7, 1)] + \
                      [date(year=2018, month=2, day=d) for d in range(12, 17, 1)] + \
                      [date(year=2018, month=3, day=d) for d in range(26, 32, 1)] + \
                      [date(year=2018, month=4, day=d) for d in range(1, 7, 1)] + \
                      [date(year=2018, month=5, day=d) for d in range(22, 32, 1)] + \
                      [date(year=2018, month=6, day=d) for d in range(1, 3, 1)] + \
                      [date(year=2018, month=7, day=d) for d in range(26, 32, 1)] + \
                      [date(year=2018, month=8, day=d) for d in range(1, 32, 1)] + \
                      [date(year=2018, month=9, day=d) for d in range(1, 9, 1)] + \
                      [date(year=2018, month=10, day=d) for d in range(29, 32, 1)] + \
                      [date(year=2018, month=11, day=d) for d in range(1, 3, 1)] + \
                      [date(year=2018, month=12, day=d) for d in range(24, 32, 1)] + \
                      [date(year=2019, month=1, day=d) for d in range(1, 6, 1)] + \
                      [date(year=2019, month=4, day=d) for d in range(15, 28, 1)] + \
                      [date(year=2019, month=6, day=d) for d in range(11, 22, 1)] + \
                      [date(year=2019, month=7, day=d) for d in range(29, 32, 1)] + \
                      [date(year=2019, month=8, day=d) for d in range(1, 32, 1)] + \
                      [date(year=2019, month=9, day=d) for d in range(1, 11, 1)] + \
                      [date(year=2019, month=10, day=d) for d in range(28, 32, 1)] + \
                      [date(year=2019, month=12, day=d) for d in range(23, 32, 1)]

if __name__ == '__main__':
    df_trips = create_synthetic_data(known_locations=KNOWN_LOCATIONS,
                                     travel_time_dict=TRAVEL_TIME,
                                     location_scatter=LOCATION_SCATTER,
                                     departure_time_scatter=DEPARTURE_TIME_SCATTER,
                                     travel_time_scatter=TRAVEL_TIME_SCATTER,
                                     monthly_trip=MONTHLY_TRIP,
                                     start_date=START_DATE,
                                     end_date=END_DATE,
                                     additional_holidays=ADDITIONAL_HOLIDAYS,
                                     seasonal_trip=SEASONAL_TRIP)

    df_trips.to_csv("data/synthetic_trip_data.csv",
                    index=False)
