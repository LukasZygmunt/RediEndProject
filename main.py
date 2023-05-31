
import requests as requests


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





