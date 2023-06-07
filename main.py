import argparse
import json
import logging
import sys
import requests as requests

# geo
munich = (48.15, 11.42)
badToelz = (47.76, 11.56)
landsbergAmLech = (48.05, 10.88)
pfaffenhofenAnDerInn = (48.53, 11.51)
haagInOberbayern = (48.16, 12.18)


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
    host = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation,cloudcover,windspeed_10m,winddirection_10m&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_hours,windspeed_10m_max,winddirection_10m_dominant&current_weather=true&forecast_days=3&timezone=Europe%2FBerlin"
    return host


#requests
munich_r = requests.get(create_host(munich))
badToelz_r = requests.get(create_host(badToelz))
landsbergAmLech_r = requests.get(create_host(landsbergAmLech))
pfaffenhofenAnDerInn_r = requests.get(create_host(pfaffenhofenAnDerInn))
haagInOberbayern_r = requests.get(create_host(haagInOberbayern))

# lists and dictionaries
city_requests_dict = {"munich": munich_r,
                      "badToelz": badToelz_r,
                      "landsbergAmLech": landsbergAmLech_r,
                      "pfaffenhofenAnDerInn": pfaffenhofenAnDerInn_r,
                      "haagInOberbayern": haagInOberbayern_r
                      }


def create_file(city: str):
    file_name = f"{city}.json"

    def return_city_r():
        for key, value in city_requests_dict.items():
            if key == city:
                return value

    if return_city_r().status_code == 200:
        json.dump(return_city_r().json(), open(file_name, "w", encoding="utf-8"), indent=4, sort_keys=True)
        logging.info(f"[INFO]File {file_name} is created")
    else:
        raise ConnectionError(f"{create_host(city)} replied with {return_city_r().status_code}: {return_city_r().reason}")
    return ""


def show_weather(when, where):
    filename = f"{where}.json"
    weather_now = {}
    weather = {}
    data = {}
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    if when == "now":
        weather_now["time"] = data["current_weather"]["time"]
        weather_now["temperature"] = data["current_weather"]["temperature"]
        weather_now["winddirection"] = data["current_weather"]["winddirection"]
        weather_now["windspeed"] = data["current_weather"]["windspeed"]
        return weather_now
    elif when == "today":
        day = 0
        weather["time"] = data["daily"]["time"][day]
        weather["temperature"] = data["daily"]["temperature_2m_max"][day]
        weather["winddirection"] = data["daily"]["winddirection_10m_dominant"][day]
        weather["windspeed"] = data["daily"]["windspeed_10m_max"][day]
        weather["rain_how_long"] = data["daily"]["precipitation_hours"][day]
        weather["rain"] = data["daily"]["precipitation_sum"][day]
        return weather
    elif when == "tomorrow":
        day = 1
        weather["time"] = data["daily"]["time"][day]
        weather["temperature"] = data["daily"]["temperature_2m_max"][day]
        weather["winddirection"] = data["daily"]["winddirection_10m_dominant"][day]
        weather["windspeed"] = data["daily"]["windspeed_10m_max"][day]
        weather["rain_how_long"] = data["daily"]["precipitation_hours"][day]
        weather["rain"] = data["daily"]["precipitation_sum"][day]
        return weather
    elif when == "after_tomorrow":
        day = 2
        weather["time"] = data["daily"]["time"][day]
        weather["temperature"] = data["daily"]["temperature_2m_max"][day]
        weather["winddirection"] = data["daily"]["winddirection_10m_dominant"][day]
        weather["windspeed"] = data["daily"]["windspeed_10m_max"][day]
        weather["rain_how_long"] = data["daily"]["precipitation_hours"][day]
        weather["rain"] = data["daily"]["precipitation_sum"][day]
        return weather


def choose_direction(start_place, when):
    create_file(start_place)
    create_file("badToelz")
    create_file("landsbergAmLech")
    create_file("pfaffenhofenAnDerInn")
    create_file("haagInOberbayern")
    start = show_weather(when, start_place)
    s = show_weather(when, "badToelz")
    w = show_weather(when, "landsbergAmLech")
    n = show_weather(when, "pfaffenhofenAnDerInn")
    e = show_weather(when, "haagInOberbayern")

    weather = {"rain": {"badToelz": s["rain"], "landsbergAmLech": w["rain"], "pfaffenhofenAnDerInn": n["rain"], "haagInOberbayern": e["rain"]},
               "rain_long": {"badToelz": s["rain_how_long"], "landsbergAmLech": w["rain_how_long"], "pfaffenhofenAnDerInn": n["rain_how_long"], "haagInOberbayern": e["rain_how_long"]},
               "windspeed": {"badToelz": s["windspeed"], "landsbergAmLech": w["windspeed"], "pfaffenhofenAnDerInn": n["windspeed"], "haagInOberbayern": e["windspeed"]},
               "winddirection": {"badToelz": s["winddirection"], "landsbergAmLech": w["winddirection"], "pfaffenhofenAnDerInn": n["winddirection"], "haagInOberbayern": e["winddirection"]},
               "temperature": {"badToelz": s["temperature"], "landsbergAmLech": w["temperature"], "pfaffenhofenAnDerInn": n["temperature"], "haagInOberbayern": e["temperature"]}
               }

    windspeed_temp = min(weather["windspeed"].values())
    windspeed_res = [key for key in weather["windspeed"] if weather["windspeed"][key] == windspeed_temp]

    rain_temp = min(weather["rain"].values())
    rain_res = [key for key in weather["rain"] if weather["rain"][key] == rain_temp]

    rain_long_temp = min(weather["rain_long"].values())
    rain_long_res = [key for key in weather["rain_long"] if weather["rain_long"][key] == rain_long_temp]

    temperature_temp = max(weather["temperature"].values())
    temperature_res = [key for key in weather["temperature"] if weather["temperature"][key] == temperature_temp]

    def return_same_wind():
        def return_direction(winddirection):
            if ((winddirection > 0 and winddirection <= 45) or (winddirection > 315)):
                direction = "n"
            elif (winddirection > 45 and winddirection <= 135):
                direction = "e"
            elif (winddirection > 135 and winddirection <= 225):
                direction = "s"
            elif (winddirection > 225 and winddirection <= 315):
                direction = "w"
            return direction

        if return_direction(start["winddirection"]) == "s":
           city = "badToelz"
        elif return_direction(start["winddirection"]) == "w":
           city = "landsbergAmLech"
        elif return_direction(start["winddirection"]) == "n":
           city = "pfaffenhofenAnDerInn"
        elif return_direction(start["winddirection"]) == "e":
           city = "haagInOberbayern"
        return city

    winddirection_res = []
    winddirection_res.append(return_same_wind())

    res = []

    if len(rain_res) > 1:
        if len(rain_long_res) > 1:
            if set(winddirection_res) & set(rain_long_res):
                res =  winddirection_res
                print(res)
            elif set(windspeed_res) & set(rain_long_res):
                res = windspeed_res
            elif set(temperature_res) & set(rain_long_res):
                res = temperature_res
            else:
                res = rain_long_res
        else:
            res = rain_long_res
    else:
        res = rain_res
    for r in res:
        return f"The best direction to cycle {when} is/are {r}"


# run
if __name__ == "__main__":
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s (%(filename)s)")
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    root.addHandler(handler)

    logging.info("starting up")

    parser = argparse.ArgumentParser(
        description=("parse the action")
    )

    parser.add_argument(
        "action",
        type=str,
        help="options: (now|today|tomorrow|after_tomorrow)",
    )
    parser.add_argument(
        "--city",
        type=str,
        help=("a string representing city ")
    )
    args = parser.parse_args()
    action = args.action
    if args.city:
        city = args.city

    if action == "now":
        if not args.city:
            logging.error("no --city")
            exit()
        create_file(city)
        print(show_weather("now", city))

    if action == "today":
        if not args.city:
            logging.error("no --city")
            exit()

        print(choose_direction(city, "today"))
        print(show_weather("today", city))

    if action == "tomorrow":
        if not args.city:
            logging.error("no --city")
            exit()

        print(choose_direction(city, "tomorrow"))
        print(show_weather("tomorrow", city))

    if action == "after_tomorrow":
        if not args.city:
            logging.error("no --city")
            exit()

        print(choose_direction(city, "after_tomorrow"))
        print(show_weather("after_tomorrow", city))



