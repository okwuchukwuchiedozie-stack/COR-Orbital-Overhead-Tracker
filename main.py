import datetime as dt
import os
import smtplib
import time
from dotenv import load_dotenv
import requests


load_dotenv()


OWN_EMAIL = os.getenv("EMAIL")
OWN_PASSWORD = os.getenv("EMAIL_PASSWORD")

MY_LAT = float(os.getenv("MY_LAT", 6.342450))
MY_LNG = float(os.getenv("MY_LNG", 5.633840))

ISS_API_URL = "http://api.open-notify.org/iss-now.json"
SUNRISE_API_URL = "https://api.sunrise-sunset.org/json"


def is_iss_overhead() -> bool:

    try:
        response = requests.get(url=ISS_API_URL, timeout=10)
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"⚠️ ISS tracking network telemetry failed: {error}")
        return False

    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    is_lat_near = MY_LAT - 5 <= iss_latitude <= MY_LAT + 5
    is_lng_near = MY_LNG - 5 <= iss_longitude <= MY_LNG + 5

    return is_lat_near and is_lng_near


def is_night() -> bool:

    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    try:
        response = requests.get(url=SUNRISE_API_URL, params=parameters, timeout=10)
        response.raise_for_status()

    except requests.RequestException as error:
        print(f"⚠️ Astronomy database connection failure: {error}")
        return False

    data = response.json()

    sunrise_time = dt.datetime.fromisoformat(data["results"]["sunrise"])
    sunset_time = dt.datetime.fromisoformat(data["results"]["sunset"])

    current_time_utc = dt.datetime.now(dt.UTC)

    return current_time_utc >= sunset_time or current_time_utc <= sunrise_time


def send_email() -> None:

    email_message = "Subject:Look up 🛰️\n\nThe International Space Station is zooming above you right now!"

    try:
        print("📨 Attempting connection via SMTP_SSL (Port 465)...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.login(OWN_EMAIL, OWN_PASSWORD)
            connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)
            print("🚀 Notification deployed successfully.")
            return
    except (smtplib.SMTPException, TimeoutError) as error:
        print(f"🔄 SSL link rejected ({error}). Forking alternative pipeline via TLS...")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(OWN_EMAIL, OWN_PASSWORD)
            connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)
            print("🚀 Notification deployed successfully via TLS.")
    except smtplib.SMTPException as error:
        print(f"❌ Critical Email Dispatch Failure: {error}")


if __name__ == "__main__":
    print(f"🛰️ Active Tracking System Engaged for Coordinates: ({MY_LAT}, {MY_LNG}). Checking parameters every 60s...")

    try:
        while True:
            if is_iss_overhead() and is_night():
                send_email()
            else:
                print(
                    f"⏱️ Log Check at {dt.datetime.now().strftime('%H:%M:%S')}: Conditions unfulfilled (ISS out of bounds or daylight active).")

            time.sleep(60)

    except KeyboardInterrupt:
        print("\n🛑 Tracking loop safely terminated by user. Goodbye!")
