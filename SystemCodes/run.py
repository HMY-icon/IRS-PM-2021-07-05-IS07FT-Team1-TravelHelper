from API import *
from NLP_extraction import *
import pandas as pd
from datetime import datetime, timedelta

# input departure || arrival location, then get code
s1 = input('Please describe where, when do you want to go')
location = location_extraction(s1)
date = time_extraction(s1)
print(location)
print(date)

s2 = input('How many adults in total?')
num_of_adults = number_extraction(s2)
print(num_of_adults)


departure_location=location[0]
arrival_location=location[1]
departure_airports = getLocationInfo(departure_location)
print(departure_airports)
arrival_airports = getLocationInfo(arrival_location)
print(arrival_airports)
recommend_target = getCityRecommendation(departure_airports[0]['code'])

departure_code = departure_airports[0]['code']
arrival_code = arrival_airports[1]['code']
print(departure_code)
print(arrival_code)

# get Flight
departure_date = date[0]
departure_flights = getFlightInfo(departure_code, arrival_code, departure_date)
print(departure_flights)
arrival_time = departure_flights['arrival_time'][0:10]

# get hotel
args_dict = {}
args_dict['location'] = arrival_location
args_dict['checkIn']  =arrival_time
arrival_time = datetime.strptime(arrival_time, "%Y-%m-%d")
args_dict['checkOut'] = (arrival_time + timedelta(days=1)).strftime("%Y-%m-%d") #默认住一天
args_dict['adults'] = num_of_adults[0]
args_dict['price_ceil'] = 200
args_dict['rating'] = 4
print(args_dict)
location = args_dict['location']
checkIn = args_dict['checkIn']
checkOut = args_dict['checkOut']
adults = args_dict['adults']
rating = args_dict['rating']
price_ceil = args_dict['price_ceil']
region_list, destinationID_list = getDestinationId(arrival_location)
results = {}
for i in range(len(region_list)):
    print(region_list[i])
    destinationId = destinationID_list[i]
    tmp = getHotelDetails(destinationId, checkIn, checkOut, adults, rating, price_ceil, pageNumber=1, pageSize=25,
                          sortOrder="PRICE")
    results.update(tmp)
print(results)
# get place of interst
for key in results:
    print("{}:{}".format(key,results[key]))
df = pd.DataFrame(results)
print (df)

# res = getPlaceInfo(arrival_location)
# print(res)