import requests
import re
from bs4 import BeautifulSoup
import pandas
import time

# Arguments required to validate scrape requests (i.e. create virtual web browser)
user_agents = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
session = requests.Session()  # to set up a session for virtual web browser

# Empty lists required for scrape loops
event_links = []
event_names = []
event_logos = []
country_links = []
country_names = []
country_logos = []

# Empty central dataframe
df_central = pandas.DataFrame(columns=['Event', 'Event Link', 'Event Logo',
                                       'Country', 'Country Link', 'Country Logo',
                                       'Artist', 'Artist Link', 'Song', 'Song Link'])

# Search for all high level event info (i.e. non-event specific)
event_response = session.get("https://eurovision.tv/events", headers=user_agents)
event_page = BeautifulSoup(event_response.text, "html.parser")
# Search for all countries and respective flags/logos
country_response = session.get("https://eurovision.tv/countries", headers=user_agents)
country_page = BeautifulSoup(country_response.text, "html.parser")

# Extract all event links that are for Eurovision events
for link in event_page.findAll('a',
                               attrs={'href': re.compile("^https://eurovision.tv/event/")}):
    event_links.append(link.get('href'))
# Extract all location names that are for Eurovision events
for link in event_page.findAll('img',
                               attrs={'class': re.compile("h-full m-auto")}):
    event_names.append(link.get('alt'))
# Extract all logo links that are for Eurovision events
for link in event_page.findAll('img',
                               attrs={'class': re.compile("h-full m-auto")}):
    event_logos.append(link.get('src'))

# Extract all country links
for link in country_page.findAll('a',
                                 attrs={'href': re.compile(r"https://eurovision.tv/country/")}):
    country_links.append(link.get('href'))
# Extract all country names
for link in country_page.findAll('h4',
                                 attrs={'class': re.compile("^font-bold")}):
    country_names.append(link.text.strip())
# Extract all country logos
for link in country_page.findAll('img',
                                 attrs={'src': re.compile(r"^https://static.eurovision.tv/hb-cgi/images/.*\.svg$")}):
    country_logos.append(link.get('src'))

# Create dataframes
df_event = pandas.DataFrame(list(zip(event_names, event_links, event_logos)),
                            columns=['Event', 'Event Link', 'Event Logo'])
df_country = pandas.DataFrame(list(zip(country_names, country_links, country_logos)),
                              columns=['Country', 'Country Link', 'Country Logo'])
df_event = df_event.set_index('Event')
df_country = df_country.set_index('Country')

# Loop through each event to find required information information
for year in range(len(event_links)):

    # Generate empty lists
    year_country_names = []
    year_artist_links = []
    year_artist_names = []
    year_song_names = []

    # Identify which event is active
    activeEvent = event_names[year]

    time.sleep(1)  # wait one second to avoid site timeouts

    # Try statement to check whether string argument is a typical URL structure
    try:
        sheet = session.get(event_links[year]+"/participants/", headers=user_agents)
    except requests.exceptions.MissingSchema:
        print("Event "+str(year+1)+" of "+str(len(event_links))+" skipped. URL: "+"not found")
        continue

    # Skip URL if not successful response from site
    if sheet.status_code != 200:
        print("Event "+str(year+1)+" of "+str(len(event_links))+" skipped. URL: "+event_links[year]+"/participants/")
        continue

    activeSheet = BeautifulSoup(sheet.text, "html.parser")

    # Extract country info
    for link in activeSheet.findAll('a',
                                    attrs={'href': re.compile("^https://eurovision.tv/country/")}):
        year_country_names.append(link.text.strip())

    # Extract all participant artist info
    for link in activeSheet.findAll('div',
                                    attrs={'class': re.compile("w-full md:w-1/3 lg:w-1/4 flex")}):
        if link.a.get('href').find("participant") == -1:
            year_artist_links.append(float('nan'))
        else:
            year_artist_links.append(link.a.get('href'))

    for link in activeSheet.findAll('h4',
                                    attrs={'class': re.compile("^text-xl")}):
        year_artist_names.append(link.text.strip())
    for link in activeSheet.findAll('div',
                                    attrs={'class': re.compile("w-full md:w-1/3 lg:w-1/4 flex")}):
        year_song_names.append(link.text.strip().split("\n")[-1])

    # Convert into dataframe, indexed by active event
    df_year = pandas.DataFrame(list(zip(year_country_names,
                                        year_artist_names, year_artist_links, year_song_names)),
                               columns=['Country',
                                        'Artist', 'Artist Link', 'Song'])
    df_year['Event'] = activeEvent

    # Append dataframe to central dataframe
    df_central = df_central.append(df_year, ignore_index=True)

    print("Event "+str(year+1)+" of "+str(len(event_links))+" completed: "+activeEvent)

# Fill in blanks (i.e. 'nan' values), where possible, in central dataframe
df_central = df_central.set_index('Event')
df_central.update(df_event)
df_central.reset_index(inplace=True)
df_central = df_central.set_index('Country')
df_central.update(df_country)
df_central.reset_index(inplace=True)

# Loop through artist pages to find song links (where possible)
for song in range(len(df_central)):

    time.sleep(1)  # wait one second to avoid site timeouts

    # Try statement to check whether string argument is a typical URL structure
    try:
        artist = session.get(df_central['Artist Link'][song], headers=user_agents)
    except requests.exceptions.MissingSchema:
        print("Song "+str(song+1)+" of "+str(len(df_central))+" skipped. URL: "+"not found")
        continue

    # Skip URL if not successful response from site
    if artist.status_code != 200:
        print("Song "+str(song+1)+" of "+str(len(df_central))+" skipped. URL: "+df_central['Artist Link'][song])
        continue

    activeArtist = BeautifulSoup(artist.text, "html.parser")

    # Extract Youtube song link
    for link in activeArtist.findAll('a',
                                     attrs={'href': re.compile(r"https://youtube.com/watch")}):
        df_central['Song Link'][song] = link.get('href')

    print("Song "+str(song+1)+" of "+str(len(df_central))+" complete: "+df_central['Song'][song])

# Save document as .csv
df_central.to_csv('vision.csv', index=False)
