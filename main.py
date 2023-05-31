
import requests as requests

def create_host(city_geo):
    latitude = city_geo[0]
    longitude = city_geo[1]
    host = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation,rain,showers,snowfall,cloudcover,windspeed_10m,winddirection_10m&daily=temperature_2m_max,temperature_2m_min,rain_sum,showers_sum,snowfall_sum,windspeed_10m_max,windgusts_10m_max,winddirection_10m_dominant&forecast_days=3&timezone=Europe%2FBerlin"
    return host


# geo
munich_geo = (48.15, 11.42)
badToelz_geo = (47.76, 11.56)
landsbergAmLech_geo = (48.05, 10.88)
pfaffenhofenAnDerInn_geo = (48.53, 11.51)
haagInOberbayern_geo = (48.16, 12.18)

munich = requests.get(create_host(munich_geo))
badToelz = requests.get(create_host(badToelz_geo))
landsbergAmLech = requests.get(create_host(landsbergAmLech_geo))
pfaffenhofenAnDerInn = requests.get(create_host(pfaffenhofenAnDerInn_geo))
haagInOberbayern = requests.get(create_host(haagInOberbayern_geo))

# run
if __name__ == "__main__":
    pass

munich_json = munich.json()
munich_file = "munich.json"

city_list = {}
city_list

# status escape must to be
if munich.status_code == 200:
    json.dump(munich_json, open(munich_file, "w", encoding="utf-8"), indent=4, sort_keys=True)
else:
    raise ConnectionError(f"{create_host(munich_geo)} replied with {munich.status_code}: {munich.reason}")



