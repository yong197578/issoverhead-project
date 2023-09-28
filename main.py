import requests
from datetime import datetime
import smtplib
import time
MY_LAT = 33.160530
MY_LONG = -96.708250

def is_iss_above():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_longitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_latitude <= MY_LONG + 5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <=sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_above() and is_night():
        my_email = "my gmail" #Put your email
        password = "gmail application password" #Application pw for gmail
        with smtplib.SMTP("stmp.gmail.com") as connection:
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject: ISS is above!\n\n You need to look up! ISS is passing!"
            )
