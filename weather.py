import requests
import json

s = 290000
if 11000<=s<=90000:
    AREAS_CODE = format(s,"06")
else:
    AREAS_CODE = s


url = f'https://www.jma.go.jp/bosai/forecast/data/forecast/{AREAS_CODE}.json'
res =requests.get(url)

data = json.loads(res.text)


i=0#天気と降水確率のareaの要素

area1 = data[0]["timeSeries"][0]["areas"][i]["area"]["name"]
print(area1)#地域名1

weather_code = data[0]["timeSeries"][0]["areas"][i]["weatherCodes"][0]
#print(weather_code)#天気コード
wc=int(weather_code)
#天気の分類とラベル付け
if 100<= wc <199:
    print("晴れ")
    weather_label="晴れ"
elif 200<= wc <299:
    print("曇り")
    weather_label="曇り"
elif 300<= wc <399:
    print("雨")
    weather_label="雨"
else:
    print("雪")
    weather_label="雪"


rainpc = data[0]["timeSeries"][1]["areas"][i]["pops"]
print(rainpc)#降水確率（6時間毎）

j=0#気温のareaの要素

area2 = data[1]["tempAverage"]["areas"][j]["area"]["name"]
print(area2)#地域名2

maxtemper = data[1]["tempAverage"]["areas"][j]["max"]
maxtemp=float(maxtemper)
print(maxtemp)#最高気温

mintemper= data[1]["tempAverage"]["areas"][j]["min"]
mintemp=float(mintemper)
print(mintemp)#最低気温


maxtempave=10  #直近1ヶ月の最高気温
mintempave=4  #直近1ヶ月の最低気温

hot_level = abs(int(maxtemp) - maxtempave)
cold_level = abs(int(mintemp) - mintempave)
bigger_level = max(hot_level,cold_level)

if bigger_level>2.5:
    if weather_label =="晴れ"or"曇り":
        if hot_level >= cold_level:
            if maxtemp >= maxtempave:
                temp_label="hot_label"
            else:
                temp_label="cold_label"

        else:
            if mintemp < mintempave:
                temp_label="cold_label"
            else :
                temp_label="hot_label"
        
    else:
        if hot_level <= cold_level:
            if mintemp <= mintempave:
                temp_label="cold_label"
            else :
                temp_label="hot_label"

        else :
            if maxtemp > maxtempave:
                temp_label="hot_label"
            else:
                temp_label="cold_label"

    print(temp_label)

else:
    print("ラベルなし")
