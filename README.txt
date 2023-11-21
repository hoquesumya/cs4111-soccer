PSQL server is assocaited with the account with uni: sh4242

URL of webapp: 

Parts implemented from proposal:
All user interaction with the database discussed in the proposal was implemented. The website serves as a frontend for a
simplified database of select soccer teams and competitions, as well as limited news functionality. The user can query soccer 
data according to different entities or attributes of each entity mentioned in the proposal. Some examples include: 
favorite teams to give players and player statistics, favorite competitions to generate games, etc.


Parts not implemented from proposal:
We did not implement the interaction with ESPN API for web scraping to generate additional realistic data, as
the data we added to our database for Part 2 of the project was significant and realistic, so there was no use
for additional data. The interaction was also quite challenging and we decided to skip it.

Interesting web pages:
1- the players webpage provides functionality to filter the list of players in the database based on membership to 
teams, in-field positions, and participation in competitions. This is interesting since the filter input is used to
generate the query which is sent to the database. Additionally, the players can based

2- the competitions webpage is interesting because it provides the user with ways to fetch information about competitions, 
which are the most 'general' entity in our ER design, and all associated sub-entities such as teams, games, etc. The user
input is used in the queries sent to the database.

AI Tools:
ChatGPT was used to help with designing UI elements in HTML such as tables and buttons for the games/players/coaches webpages,
as well as some basic debugging with the Flask routing and decorators used as well as javascript AJAX and JQuery for API calls.

ADDITIONAL SECTION: AJAX/JQUERY CALLS
We decided to use AJAX/JQUERY for all our API calls due to familiarity. Here is a summary of the calls:

get_coaches():
- Purpose: Fetches coach data.
- Endpoint: '/c/coaches'.
- Trigger: Clicking the coaches button on the home page.
- Location: home page

get_competition():
- Purpose: Retrieves competition data.
- Endpoint: '/competition' webpage.
- Trigger: Clicking competitions button on home page.
- Location: home page

get_games():
- Purpose: Retrieves all game data.
- Endpoint: /g/games'
- Trigger: Clicking games button on home page.
- Location: home page


get_news():
- Purpose: Fetches news data.
- Endpoint: /n/news.
- Trigger: Clicking games button on home page.
- Location: home page

'populatefilters.js'
- Purpose: Populates dropdowns based on the current URL and send 
  filtering parameters from user input to server.py
- Endpoint: players page exited
- Trigger: Page load and user interaction for filters.
- Location: 'players.html'


get_playerstats(button):
- Purpose: Fetches player statistics based on the selected player.
- Endpoint: /p/players
- Trigger: clicking on player
- Location: /p/playerstats

get_players():
- Purpose: Fetches player data.
- Endpoint: /p/players
- Trigger: Clicking on the players button.
- Location: homepage

