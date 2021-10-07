# Mobility Data Creator 

------
## Why Mobility Data?
Regardless of the means of transportation, 
individual human mobility is an aspect of our modern society with utmost relevance.
In order to maintain a mobility system without severe problems or to improve its efficiency and convenience, 
data-driven services based on mobility data of individual humans increasingly gain importance.
The availability of such data, however, is limited due to data privacy issues.
This concise tool helps to create synthetic mobility data in a realistic way 
that can then be used for all kinds of predictive tasks.  

-----------
## How Does It Work?
To run the `mobility-data-creator`, you essentially need to provide

- a set of [known locations](data/known_locations.json), and
- the [travel times](data/travel_times.json) in between those,

in the [`data`](data) directory. 
When running the [`main.py`](main.py) script, a [CSV-file](data/synthetic_trip_data.csv) 
is created containing a sequence of journeys, e.g. trips taken by car.
The columns represent the following information:

|Name    |Description|
|---------------|---------------------------------------------|
|_gps_start_lat_|    Latitude of GPS position at start of trip|
|_gps_start_lon_|    Longitude of GPS position at start of trip|
|_t_start_|          Start time of trip as UTC time code in Milliseconds|
|_t_end_|            End time of trip as UTC time code in Milliseconds|
|_gps_end_lat_|      Latitude of GPS position at end of trip|
|_gps_end_lon_|      Longitude of GPS position at end of trip|

For the already provided example data, the created raw data points are visualized here:
![](data/raw_mobility_data.PNG)
In addition, the logic of how the sequence of journeys should be appended can be 
adapted in [`trip_creation.py`](trip_creation.py).

---------
## For What Can It Be Useful?
The [data set](data/synthetic_trip_data.csv) presented here was used for a study on 
estimating the parking duration of vehicles, see here.
[comment]: <> (TODO: add link to paper here!)
Beyond this, however, a variety of further use cases, e.g. predicting the next place to visit, is conceivable.
For all contributions that supported this research, many thanks also goes to

- [Kaleb Phipps](https://github.com/kalebphipps) (Karlsruhe Institute of Technology)
- [Benjamin Briegel](https://github.com/bbriegel) (Mercedes-Benz AG)
- [Veit Hagenmeyer](https://www.iai.kit.edu/Ansprechpersonen_1213.php) (Karlsruhe Institute of Technology)
- [Ralf Mikut](https://www.iai.kit.edu/Ansprechpersonen_1030.php) (Karlsruhe Institute of Technology)

---------
## Where Can I Contribute?
If you find a use case for which the `mobility-data-creator` or the provided data can be helpful, 
feel free to use it.
Furthermore, if adaptions of the source code my help to improve this tool, 
you are more than welcome to open an issue and discuss on how to integrate your suggestions. 

For further questions, please contact [Karl Schwenk](https://github.com/KarlSchwenk).
