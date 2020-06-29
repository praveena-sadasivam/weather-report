from flask import Flask,render_template,request
import requests
import time
import database
from database import insert_into_weather,get_value

#flask object
app=Flask(__name__,
template_folder="client/template")



#to get weather details from app
def get_weather(city):
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
    else:
        location = 'chennai'#default city = chennai
    from datetime import datetime, timedelta
    #geting value from db
    weather_value=get_value(location)
    #if value exist
    if len(weather_value)!=0:
        time=weather_value[0][2]
        old = datetime.fromtimestamp(time)
        now = datetime.now()
        #checking if value is one day older
        #if within 24 hrs then
        if now-timedelta(hours=24) <= old <= now+timedelta(hours=24):
            description=weather_value[0][0]
            temp=weather_value[0][1]
            print("\n WEATHER REPORT updated using DB")
        
        else:
        #if more than one day then  get value from app
            print("3")
            value=get_weather(location)
            description=value[0]
            temp=value[1]
            time=value[2]
            insert_into_weather(location,description,temp,time)
            print("\n WEATHER REPORT updated using app")
    else:
        
        print("3")
        value=get_weather(location)
        description=value[0]
        temp=value[1]
        time=value[2]
        insert_into_weather(location,description,temp,time)
        print("\n WEATHER REPORT updated using app")
    print("\nweather report - "+"\nlocation : "+str(location)+"\n description : "+str(description)+"\ntemperature : "+str(temp)+"\n")
    return render_template("weather.html",location=location,description=description,temp=temp) 



if __name__ == '__main__':
    app.run(debug=True,port=5000)
