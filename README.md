# translinkbot
Reddit bot to provide upcoming NI Railways train departure times to a provided station when invoked.

## Availability
At the moment the bot will only be available when running from my personal machine.

Also note that the bot will talk to a proxy I set up to get the relevant information, which is hosted for free on Heroku, and thus will be unavailable in the last couple of days of some months.

## Usage
Comment in any submission in `r/northernireland` with:
`!translinkbot <station name>`

Provided the rate limit is removed you should get a response within a few seconds.

## Recognised Stations
Station names are compared to a response from the [OpenData API](https://www.opendatani.gov.uk/dataset/real-time-rail-stations-arrivals-and-departures/resource/490fe701-0e7b-4030-a4b0-9ede8c0d85cf) and most should be recognised without issue.

Variations accounted for include:
- Derry, Londonderry, Derry/Londonderry and Waterside will all refer to the same station
- Lanyon Place and Belfast Central will refer to the same station
- Great Victoria Street and Great Victoria St will refer to the same station
