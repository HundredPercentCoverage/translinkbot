import praw
import requests
import json
import os

# Take a few variations into consideration
variations = {
  "Derry": "Londonderry",
  "Derry/Londonderry": "Londonderry",
  "Waterside": "Londonderry",
  "Lanyon Place": "Belfast Central",
  "Great Victoria Street": "Great Victoria St",
  "Mossley": "Mossley West"
}

# Log in to Reddit
print('Logging in to Reddit...')
reddit = praw.Reddit(
  client_id = os.environ['TRANSLINK_BOT_CLIENT_ID'],
  client_secret = os.environ['TRANSLINK_BOT_CLIENT_SECRET'],
  user_agent = os.environ['TRANSLINK_BOT_USER_AGENT'],
  username = os.environ['TRANSLINK_BOT_USERNAME'],
  password = os.environ['TRANSLINK_BOT_PASSWORD']
)

subreddit = reddit.subreddit('northernireland')

keyphrase = '!translinkbot'

print('Retrieving stations...')
stations_list = requests.get('https://translink-proxy.herokuapp.com/stations').json()

station_code = None

print("Monitoring comments...")
for comment in subreddit.stream.comments():
  if keyphrase in comment.body:
    try:
      requested_station = comment.body.replace(keyphrase, '').lstrip(' ')
      adapted_requested_station = requested_station
      print('Received request for "{}"'.format(requested_station))

      # Take variations int account
      if requested_station in variations:
        adapted_requested_station = variations[requested_station]

      for station in stations_list:
        if station["name"].lower() == adapted_requested_station.lower():
          station_code = station["code"]

      if station_code is not None:
        station_info = requests.get('https://translink-proxy.herokuapp.com/station/{}'.format(station_code)).json()

        # Check if there are actually services
        try:
          services = station_info['StationBoard']['Service']

          # API will return a list if multiple trains are coming, otherwise it will just return a single dict
          if isinstance(services, dict):
            services = [services]

          reply = "Bleep, bloop. I am a bot. Here is a list of upcoming departures for: **" + requested_station + "**\n\n"

          reply += 'Destination | Scheduled | Expected | Status\n:------:|:------:|:------:|:------:\n'

          for service in services:
            destination = service['Destination1']['$']['name']
            scheduled_departure = service['DepartTime']['$']['time']
            expected_departure = service['ExpectedDepartTime']['$']['time']
            status = service['ServiceStatus']['$']['Status']

            if destination != '**Terminates**':
              reply += destination + ' | ' + scheduled_departure + ' | ' + expected_departure + ' | ' + status + '\n'

          reply += "\nA mobile-friendly web app for this can be found [here](https://hundredpercentcoverage.github.io/translink-trains/).\n"
          reply += "\n[Readme](https://github.com/HundredPercentCoverage/translinkbot)\n"

          comment.reply(reply)
        except:
          comment.reply('Bleep, bloop. There are no trains due at **' + requested_station + '** for at least 90min.')
      else:
        print('Station not recognised. Sending reply...')
        comment.reply("I'm sorry, I don't recognise that station!")
    except:
      print('Fell afoul of rate limit.')
    


