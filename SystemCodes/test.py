import streamlit as st
from API import *
from NLP_extraction import *
from datetime import datetime, timedelta
import pandas as pd
from PIL import Image


#@st.cache
image_ = Image.open('images/pexels-leah-kelley-185933.jpg')
st.image(image_, use_column_width=True)
st.title('Hi, travelers. ')
st.title('This is a helper for your trip.')
# 这里提取输入的出发日期与起始、目标地点
txt = st.text_area('Please tell us where/when do you want to go',
                   '''e.g. I want to leave from Beijing to Shanghai on 24 Dec 2021''')
location = location_extraction(txt)
departure_location = location[0]
departure_airports = getLocationInfo(departure_location)  # 获取IATA code
departure_code = departure_airports[0]['code']

if(len(location)==1):   # 如果没有目标，就推荐一个
    arrival_location = getCityRecommendation(departure_code)
else:
    arrival_location = location[1]

arrival_airports = getLocationInfo(arrival_location)
arrival_code = arrival_airports[1]['code']
date = time_extraction(txt)
# 这里选择人数、机舱等级、单程还是往返
txt = st.text_area('Please tell us some details about your journey',
                   '''e.g. I prefer Economic cabin. We have three people in total. This is a single trip''')
num_of_adults = number_extraction(txt)
# st.sidebar.header('Your cabin selection')
# selected_cabin = st.sidebar.selectbox('Cabin', ['Economic', 'Businiess', 'First Class'])
cabin_level = 'Economic'
single_round = 'Single'

# 这里展示全部的配置信息

if (st.button("Let's go")):
    st.header('This is detailed information about your trip')
    col1, col2, col3 = st.columns(3)
    col1.metric("Departure location", departure_location)
    col2.metric("Arrival location",arrival_location)
    col3.metric("Departure Date",date[0])
    col1, col2, col3 = st.columns(3)
    col1.metric("People in total", num_of_adults[0])
    col2.metric("Cabin Level",cabin_level)
    col3.metric("Single/Round Trip",single_round)

    if (single_round=='Round'):
        pass

# 运行API

    departure_date = date[0] # 获取航班
    departure_flights = getFlightInfo(departure_code, arrival_code, departure_date)
    print(departure_flights)
    arrival_time = departure_flights['arrival_time'][0:10]

    args_dict = {}
    args_dict['location'] = arrival_location
    args_dict['checkIn'] = arrival_time
    arrival_time = datetime.strptime(arrival_time, "%Y-%m-%d")
    args_dict['checkOut'] = (arrival_time + timedelta(days=1)).strftime("%Y-%m-%d")  # 默认住一天
    args_dict['adults'] = num_of_adults[0]
    args_dict['price_ceil'] = 500
    args_dict['rating'] = 3
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

    place = getPlaceInfo(arrival_location) # get place of interst



# 将结果展示到网页
    st.title('This is what we plan for you. ')

    my_bar = st.progress(0)
    

    st.header('Your Flight')
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Take off time", departure_flights['departure_time'][5:16])
    col2.metric("Landing time",departure_flights['arrival_time'][5:16])
    col3.metric("Duration",departure_flights['duration'])
    col1, col2 = st.columns(2)
    col1.metric('Flight cost',departure_flights['price'])
    col2.metric('Airline',departure_flights['airline'])

    my_bar = st.progress(0)
    

    st.header('Your Hotel')

    df = pd.DataFrame(results)
    st.dataframe(df.T)

    my_bar = st.progress(0)
    # for percent_complete in range(100):
    #     my_bar.progress(percent_complete + 1)

    st.header('Your Fun ')
    for i in range(0,len(place)):
        if(i%3 == 0):
            col1,col2,col3 = st.columns(3)
            with col1:
                try:
                    st.image(place[i]['image_link']['url'],caption=place[i]['name'],use_column_width=True)
                    i = i+1
                except:
                    break
            with col2:
                try:
                    st.image(place[i]['image_link']['url'], caption=place[i]['name'],use_column_width=True)
                    i=i+1
                except:
                    break
            with col3:
                try:
                    st.image(place[i]['image_link']['url'], caption=place[i]['name'],use_column_width=True)
                except:
                    break
    st.title('Wish you have a nice trip! :-)')
else:
        st.write("Let's Go")





