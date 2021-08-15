import datetime as dt
import requests
from bs4 import BeautifulSoup
import json

# Didn't use selenium because I didn't want to.

html = requests.get('https://www.muslimpro.com/en/prayer-times').text
soup = BeautifulSoup(html, 'html.parser')

# Find the times and prayers in diffrent lists
times = soup.find_all(class_='jam-solat')
prayers = soup.find_all(class_='waktu-solat')

# Placeholder
namaz_times = {}

# Create a dictionary with prayer names as keys and times as values
for prayer in range(len(prayers)):
    namaz_times[prayers[prayer].getText()] = times[prayer].getText()

now_hour = int(dt.datetime.now().strftime("%H"))

# Placeholders
closest_prayer_diffrence = 1000
closest_prayer = None

# Loop through each prayer in the dict and find out which one is the closest from now
for prayer in namaz_times:
    namaz_hour = int(namaz_times[prayer].split(":")[0])

    if namaz_hour - now_hour < closest_prayer_diffrence and namaz_hour - now_hour > 0:
        closest_prayer_diffrence = namaz_hour - now_hour
        closest_prayer = prayer

# Break the loop if its in the same hour because obiously its the closest prayer.
    if namaz_hour == now_hour:
        namaz_minute = int(namaz_times[prayer].split(":")[1])
        now_minute = int(dt.datetime.now().strftime("%M"))
        if namaz_minute > now_minute:
            closest_prayer = prayer
            break

# If its passed isha than its none meaning that the next prayer is going to be fajr
if closest_prayer is None:
    closest_prayer = "Fajr"

closest_prayer_dic = namaz_times[closest_prayer]

now = dt.datetime.now()

closest_prayer_time = dt.datetime(year=now.year, 
                        month=now.month,
                        day=now.day,
                        hour=int(closest_prayer_dic.split(":")[0]), 
                        minute=int(closest_prayer_dic.split(":")[1]))
time_diffrence = closest_prayer_time - now

# Create a nested dicitonary for the closest prayer
namaz_times["closest_prayer"] = {
    "namazName": closest_prayer,
    # absolutee value in case its negative for Fajr
    # camel case for js
    # microseconds for the settimeout function
    "microsecondsLeft": abs(dt.timedelta.total_seconds(time_diffrence) * 1000)
}

# create the json file
with open("namaz.json", "w") as file:
    json.dump(namaz_times, file, indent=4)
