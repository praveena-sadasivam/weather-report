from flask import Flask,render_template,request
import requests
import time
import database
from database import insert_into_weather,get_value_from_DB,print_val,delete_record

#flask object
app=Flask(__name__,
template_folder="client/template",
static_folder="client/static")



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
    if request.method == 'POST':
        location = request.form['city']
        from datetime import datetime, timedelta
        #geting value from db
        weather_value=get_value_from_DB(location.casefold())
        #if value exist
        if len(weather_value)!=0:
            print("\nweather report values for this location already exist in db\n")
            time=weather_value[0][2]
            old = datetime.fromtimestamp(time)
            now = datetime.now()
            #checking if value is one day older
            #if within 24 hrs then
            if now-timedelta(hours=24) <= old <= now+timedelta(hours=24):
                print("\nweather report values are not yet 24 hrs older\n")
                description=weather_value[0][0]
                temp=weather_value[0][1]
                print("\n So, WEATHER REPORT updated using DB\n")
        
            else:
                print("\nweather report values for this location is 24 hrs older\n")
                #if value is one day older
                value=get_weather_record_from_app(location.casefold())
                description=value[0]
                temp=value[1]
                time=value[2]
                delete_record(location.casefold())
                insert_into_weather(location.casefold(),description,temp,time)
                print("\nSo, WEATHER REPORT updated using app")
        else:
            print("\nweather report values for this location does not already exist in db\n")
            #getting value for first time
            value=get_weather_record_from_app(location.casefold())
            description=value[0]
            temp=value[1]
            time=value[2]
            insert_into_weather(location.casefold(),description,temp,time)
            print("\nSO, WEATHER REPORT updated using app and report values are added into DB")
        temp_celsius=kelvin_to_celsius(float(temp))
        print("\nweather report - "+"\nlocation : "+str(location.casefold())+"\n description : "+str(description)+"\ntemperature : "+str(temp)+"\n")
        return render_template("weather.html",location=location.casefold(),description=description,temp=temp,temp_celsius=temp_celsius)
    else:
        print("\nsearching weather report based on user input\n")
        return render_template("weather.html")

def kelvin_to_celsius(temp):
    return(round(temp-273.15,2))


if __name__ == '__main__':
    app.run(debug=True,port=5000)
