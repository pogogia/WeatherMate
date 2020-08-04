from flask import Flask, render_template, request
import requests

app = Flask(__name__,static_url_path='')


@app.route('/', methods= ['POST', 'GET'])
def weather():
    if request.method == 'POST':
        city_name = request.form['city']
    else:
        city_name = 'Delhi'

    api_key = '462fcca739d9fde00ed77eace0f56f18'
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    source_url = base_url + "q=" + city_name + "&appid=" + api_key
    response = requests.get(source_url)
    x =response.json()

    if x['cod'] == '404':
        return render_template('error.html',data=x)

    week_api_key = 'hobMSRLq4lblEwRGo3kV6oGxeROODPB8'
    loc_url = 'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=' + week_api_key + '&q=' + city_name
    acc_response = requests.get(loc_url)
    response_list = acc_response.json()
    weather_accu_base_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/'
    weather_accu_url = weather_accu_base_url + response_list[0]['Key'] + '?apikey=' + week_api_key + '&language=en-us'
    week_response = requests.get(weather_accu_url)
    week_response_dict = week_response.json()

    final_week_data_dict = {}

    for i in range(0,5):
        final_week_data = {
                            "city" : city_name,
                            "date" : week_response_dict["DailyForecasts"][i]["Date"][:10],
                            "max_temp" : round((week_response_dict["DailyForecasts"][i]["Temperature"]["Maximum"]["Value"] - 32 ) * (5/9), 2),
                            "min_temp": round((week_response_dict["DailyForecasts"][i]["Temperature"]["Minimum"]["Value"] - 32) * (5 / 9), 2),
                            "precipitation": week_response_dict["DailyForecasts"][i]["Day"]["HasPrecipitation"],
                            "cloudiness": week_response_dict["DailyForecasts"][i]["Day"]["IconPhrase"],
                            "week_description": week_response_dict["Headline"]["Text"],
                            "cloud_icon": week_response_dict["DailyForecasts"][i]["Day"]["Icon"]

                         }
        final_week_data_dict.update({'Day' + str(i) : final_week_data})

    if x['cod'] != "404":
        final_data = {
            "city" : x['name'],
            "temp": round((x['main']['temp'] - 273.15),2),
            "pressure": x['main']['pressure'],
            "humidity": x['main']['humidity'],
            "wind_speed": x["wind"]["speed"],
            "icon": x["weather"][0]["icon"]

        }

        final_data.update(final_week_data_dict)
        return render_template('index.html',data=final_data)

    else:
        return render_template('error.html')


if __name__ == '__main__':
        app.run(debug=True)