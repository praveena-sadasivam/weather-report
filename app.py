from flask import Flask,render_template,request
import requests
import time
import database
import sys
from database import insert_into_weather,get_value_from_DB,print_val,delete_record

#flask object
app=Flask(__name__,
template_folder="client/template",
static_folder="client/static")

def time_stamp_operation(weather_value):
    from datetime import datetime, timedelta
    time=weather_value[0][2]
    old = datetime.fromtimestamp(time)
    now = datetime.now()
    #checking if value is one day older
    #if within 24 hrs then
    if now-timedelta(hours=24) <= old <= now+timedelta(hours=24):
        return True
    else:
        return False

def value_is_outdated_get_from_app(location):
    value=get_weather_record_from_app(location.casefold())
    description=value[0]
    temp=value[1]
    time=value[2]
    delete_record(location.casefold())
    insert_into_weather(location.casefold(),description,temp,time)
    return[description,temp]


def new_location_get_value_from_app(location):
    value=get_weather_record_from_app(location.casefold())
    description=value[0]
    temp=value[1]
    time=value[2]
    insert_into_weather(location.casefold(),description,temp,time)
    return[description,temp]
    


#to get weather details from app
def get_weather_record_from_app(city):
    import time
    url="http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=c3705557af5a4cb6e34319a2201b3ef5"
    json_response=requests.get(url).json()
    
    weather_description=json_response["weather"][0]["description"]
    temp=json_response["main"]["temp"]
    time=time.time()
    return[weather_description,temp,time]

#main function
@app.route("/",methods =['POST', 'GET'])
def weather():
    try:
        if request.method == 'POST':
            location = request.form['city']
            weather_value=get_value_from_DB(location.casefold()) #geting value from db
            if len(weather_value)!=0:#if value exist
                print("\nweather report values for this location already exist in db\n")
                if time_stamp_operation(weather_value):
                    print("\nweather report values are not yet 24 hrs older\n")
                    description=weather_value[0][0]
                    temp=weather_value[0][1]
                    print("\n So, WEATHER REPORT updated using DB\n")
                else:
                    print("\nweather report values for this location is 24 hrs older\n")
                    app_value=value_is_outdated_get_from_app(location)
                    description=app_value[0]
                    temp=app_value[1]
                    print("\nSo, WEATHER REPORT updated using app")
            else:
                print("\nweather report values for this location does not already exist in db\n")
                app_value=new_location_get_value_from_app(location)
                description=app_value[0]
                temp=app_value[1]
                print("\nSO, WEATHER REPORT updated using app and report values are added into DB")
            print("\nweather report - "+"\nlocation : "+
            str(location.casefold())+"\n description : "+str(description)+"\ntemperature : "+str(temp)+"\n")
            return render_template("weather.html",location=location.casefold(),description=description,temp=temp,temp_celsius=kelvin_to_celsius(float(temp)))
        else:
            print("\nsearching weather report based on user input\n")
            return render_template("weather.html")
    except:
        print("city name not found")
        return render_template("invalid.html")


def kelvin_to_celsius(temp):
    return(round(temp-273.15,2))


if __name__ == '__main__':
    app.run(debug=True,port=5000)
