from recognizers_number import recognize_number, Culture # 提取数字
from recognizers_date_time import recognize_datetime # 提取时间
from flashgeotext.geotext import GeoText #提取地点


def time_extraction(s):
    res = recognize_datetime(s,Culture.English)
    list = []
    for item in res:
        r = item.__dict__
        print(r)
        time = r['resolution']['values'][0]['value']
        list.append(time)
        break
    return list

def number_extraction(s):
    res = recognize_number(s, Culture.English)
    list = []
    for item in res:
        print(item.__dict__)
        r = item.__dict__
        number = int(r['resolution']['value'])
        list.append(number)
    return list

def location_extraction(s):
    geotext = GeoText()
    res = geotext.extract(input_text=s, span_info=True)
    locations = []
    for key in res:
        for _ in res[key]:
            locations.append(_)
    return locations







