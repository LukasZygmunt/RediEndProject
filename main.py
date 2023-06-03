import json
import logging
import requests as requests


def input_new_city_geo():
    city_geo_latitude = float(input("please input latitude e.g. 48.15: "))
    city_geo_longitude = float(input("please input longitude e.g. 11.42: "))
    city_geo = (city_geo_latitude, city_geo_longitude)
    return city_geo


def input_city_name():
    city_name = str(input("please put new name of place: "))
    return city_name


def add_to_dict():
    city_requests_dict[input_city_name()] = requests.get(create_host(input_new_city_geo()))


def print_dict(dict):
    for key, value in dict.items():
        print(f"{key} = {value}")


def create_geo(latitude, longitude):
    return (latitude, longitude)


def create_host(city_geo):
    latitude = city_geo[0]
    longitude = city_geo[1]
    host = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation,rain,showers,snowfall,cloudcover,windspeed_10m,winddirection_10m&daily=temperature_2m_max,temperature_2m_min,rain_sum,showers_sum,snowfall_sum,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant&forecast_days=3&timezone=Europe%2FBerlin"
    return host


def create_file(city: str):
    file_name = f"{city}.json"

    def return_city_r():
        for key, value in city_requests_dict.items():
            if key == city:
                return value
    if return_city_r().status_code == 200:
        json.dump(return_city_r().json(), open(file_name, "w", encoding="utf-8"), indent=4, sort_keys=True)
        print(f"[INFO]File {file_name} is created")
        logging.info(f"[INFO]File {file_name} is created")
    else:
        raise ConnectionError(f"{create_host(city)} replied with {return_city_r().status_code}: {return_city_r().reason}")
    return ""


# run
if __name__ == "__main__":
    pass

# geo
munich = (48.15, 11.42)
badToelz = (47.76, 11.56)
landsbergAmLech = (48.05, 10.88)
pfaffenhofenAnDerInn = (48.53, 11.51)
haagInOberbayern = (48.16, 12.18)

#requests
munich_r = requests.get(create_host(munich))
badToelz_r = requests.get(create_host(badToelz))
landsbergAmLech_r = requests.get(create_host(landsbergAmLech))
pfaffenhofenAnDerInn_r = requests.get(create_host(pfaffenhofenAnDerInn))
haagInOberbayern_r = requests.get(create_host(haagInOberbayern))

# lists and dictionaries
city_requests_list = [munich_r, badToelz_r, landsbergAmLech_r, pfaffenhofenAnDerInn_r, haagInOberbayern_r]
city_requests_dict = {"munich" : munich_r,
                      "badToelz" : badToelz_r,
                      "landsbergAmLech" : landsbergAmLech_r,
                      "pfaffenhofenAnDerInn" : pfaffenhofenAnDerInn_r,
                      "haagInOberbayern" : haagInOberbayern_r
                      }

print(create_file("munich"))
add_to_dict()
print_dict(city_requests_dict)
