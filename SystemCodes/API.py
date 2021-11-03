import requests
def getToken():
    #get Amadeus token
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'grant_type': 'client_credentials',
            'client_id': '1qB8Bn8iGdBvNn5sEfzmKAfCdczAJfAL',
            'client_secret': 'wP7rGMR20Gia3ktf'}
    response = requests.post(url, headers=headers, data=data)
    response = response.json()  # convert to json
    token = response['access_token']
    return token

def getLocationInfo(city):
    #get city and its airport code
    url = "https://travel-advisor.p.rapidapi.com/airports/search"
    querystring = {"query": city,"locale":"en_US"}
    headers = {
        'x-rapidapi-host': "travel-advisor.p.rapidapi.com",
        'x-rapidapi-key': "20caf110e1mshea6538ea9ee83adp1f9853jsnca493b32d913"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()

    airport_list = []
    for i in range(0,len(response)):
        dic={}
        dic['code'] = response[i]['code']
        dic['airport'] = response[i]['name']
        dic['city'] = response[i]['city_name'] +','+ response[i]['country_code']
        airport_list.append(dic)
    return airport_list
    #return example
    #[{'code': 'SHA', 'airport': 'Hongqiao Airport', 'city': 'Shanghai,CN'}, {'code': 'PVG', 'airport': 'Pu Dong Airport', 'city': 'Shanghai,CN'}]

def getCityRecommendation(citycode):#subType=CITY or AIRPORT, keyword = airport code or specific city
    #recommend destination according to departure city
    token = getToken()
    url = "https://test.api.amadeus.com/v1/reference-data/recommended-locations?cityCodes={}".format(citycode)
    headers_1 = {'Authorization': 'Bearer {}'.format(token)}
    response = requests.get(url, headers=headers_1)
    response = response.json()
    response = response['data']
    res = []
    for _ in response:
        res.append({'name': _['name'], 'code': _['iataCode']})
    return res

def getFlightInfo(departure_location, arrival_location, departure_date, sort_order='PRICE', class_type='ECO', itinerary_type="ONE_WAY",number_of_passengers=1):
#sort_order: PRICE,ARRIVETIME,DEPARTTIME,TRAVELTIME
#itinerary_type : ONE_WAY, ROUND_TRIP
#class_type: ECO,BUS,PEC,FST
    url = "https://priceline-com-provider.p.rapidapi.com/v1/flights/search"
    querystring = {"sort_order":sort_order,
                   "location_departure":departure_location,
                   "date_departure":departure_date,
                   "class_type":class_type,
                   "location_arrival":arrival_location,
                   "itinerary_type":   itinerary_type,
                   "number_of_passengers": number_of_passengers
                   }
    headers = {
        'x-rapidapi-host': "priceline-com-provider.p.rapidapi.com",
        'x-rapidapi-key': "20caf110e1mshea6538ea9ee83adp1f9853jsnca493b32d913"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    # print(response)
    dic = {}
    dic['price'] = str(response['pricedItinerary'][0]['pricingInfo']['totalFare']) +' USD'
    ticketingAirline = response['pricedItinerary'][0]['pricingInfo']['ticketingAirline']
    dic['arrival_time'] = response['segment'][0]['arrivalDateTime']
    dic['departure_time'] = response['segment'][0]['departDateTime']
    dic['duration'] = str(response['segment'][0]['duration'])+' mins'
    for i in range(0, len(response['airline'])):
        if(response['airline'][i]['code']==ticketingAirline):
            dic['airline'] =response['airline'][i]['name']
            break
    return dic

def getDestinationId(location):
    url ="https://hotels4.p.rapidapi.com/locations/search"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "20caf110e1mshea6538ea9ee83adp1f9853jsnca493b32d913"
    }
    querystring = {"query":location}
    region_list = list()
    destinationID_list = list()
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    regions = response['suggestions'][0]['entities']
    for i in range(len(regions)):
        region = regions[i]['name']
        destinationID =regions[i]['destinationId']
        region_list.append(region)
        destinationID_list.append(destinationID)
    return region_list, destinationID_list


def getHotelDetails(destinationId, checkIn, checkOut, adults, rating, price_ceil, pageNumber=1, pageSize=25,
                    sortOrder="PRICE"):
    # check_in check_out format: 2020-01-15
    url = "https://hotels4.p.rapidapi.com/properties/list"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "20caf110e1mshea6538ea9ee83adp1f9853jsnca493b32d913"
    }
    querystring = {"destinationId": destinationId, "pageNumber": pageNumber, "pageSize": pageSize, "checkIn": checkIn,
                   "checkOut": checkOut, "adults1": adults, "sortOrder": sortOrder}

    results = dict()
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    hotel_info = response['data']['body']['searchResults']['results']
    # tplt = "{0:^100}\t{1:^20}\t{2:^40}\t{3:^20}\t{4:^20}\t{5:^80}"
    tplt = "{0:^100}\t{1:^20}\t{2:^40}\t{3:^20}\t{4:^20}"
    # print(tplt.format("Name", "starRating","Address", "Price", "HotelId", "Img_url"))
    # print(tplt.format("Name", "starRating","Address", "Price", "HotelId"))
    for i in range(len(hotel_info)):
        try:
            name = hotel_info[i]['name']
        except:
            name = 'None'
            pass
        try:
            starRating = hotel_info[i]['starRating']
        except:
            starRating = 'None'
            pass
        try:
            address = hotel_info[i]['address']['streetAddress']
        except:
            address = 'None'
            pass
        try:
            price = hotel_info[i]['ratePlan']['price']['current']
        except:
            price = 'None'
        try:
            supplierHotelId = hotel_info[i]['supplierHotelId']
            # img_url = getHotelImage(supplierHotelId)
            # if img_url == None:
            #     img_url = 'None'

        except:
            supplierHotelId = 'None'
            # img_url = 'None'
            pass
        # print(tplt.format(name, starRating, address, price, supplierHotelId, img_url))
        if starRating == 'None' or price == 'None':
            continue
        if int(starRating) >= rating and int(price[1:].replace(',', '')) <= price_ceil:
            tmp = dict()
            tmp["starRating"] = starRating
            tmp["address"] = address
            tmp["price"] = price
            tmp["supplierHotelId"] = supplierHotelId
            results[name] = tmp

            # print(tplt.format(name, starRating, address, price, supplierHotelId))
    return results

def getHotelImage(hotelid):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    headers = {
        'x-rapidapi-host': "travel-advisor.p.rapidapi.com",
        'x-rapidapi-key': "20caf110e1mshea6538ea9ee83adp1f9853jsnca493b32d913"
    }

    querystring = {"id":str(hotelid)}
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.json()['hotelImages'][0]["baseUrl"])

def getPlaceInfo(arrival_location):
    url ="https://hotels4.p.rapidapi.com/locations/search"
    querystring = {"query":arrival_location}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "20caf110e1mshea6538ea9ee83adp1f9853jsnca493b32d913"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    regions = response['suggestions'][0]['entities']
    for i in range(1):
        latitude = regions[i]['latitude']
        longitude = regions[i]['longitude']

    url = "https://travel-advisor.p.rapidapi.com/attractions/list-by-latlng"

    querystring = {"longitude":longitude,"latitude":latitude,"lunit":"km","currency":"RMB"}

    headers = {
        'x-rapidapi-host': "travel-advisor.p.rapidapi.com",
        'x-rapidapi-key': "20caf110e1mshea6538ea9ee83adp1f9853jsnca493b32d913"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    data = response['data']
    # print(data[0]['name'])
    res = []
    for item in data:
        dic={}
        try:
            dic['name'] = item['name']
            dic['rating'] = item['rating']
            dic['image_link'] = item['photo']['images']['original']
        except:
            continue
        res.append(dic)
    return res

