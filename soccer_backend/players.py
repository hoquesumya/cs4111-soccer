from flask import( Flask, request, render_template, g, redirect, 
                  Response, abort,jsonify,
                  make_response, Blueprint)
import os
from sqlalchemy import *
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool
import datetime
from config import engine
basedir = os.path.abspath(os.path.dirname(__file__))
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')

players = []
performancestats = []
filteredplayers = []



players_bp = Blueprint("players_list", __name__, template_folder=tmpl_dir,static_folder='../static')


@players_bp.before_request
def before_request():

  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@players_bp.teardown_request
def teardown_request(exception):
  
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass
  
  
@players_bp.route('/allplayersquery')
def allplayersquery():
  
  data =  g.conn.execute(text("""SELECT T.name FROM Player P, Team_Member T WHERE P.member_id = T.member_id;"""))
  
  g.conn.commit()
  
  
  for result in data.mappings():
    if result['name'] not in players: players.append(result['name'])
  data.close()
  return jsonify({'player': players})
  
  
@players_bp.route('/players')
def returnallplayers():
  return render_template("players.html", all_players=players)


@players_bp.route('p/playerstats', methods=['POST'])
def playerstats():
  global performancestats
  performancestats = []
  player_name = request.json
  val = f"SELECT * FROM player_stats S \
          WHERE S.member_id = (SELECT T.member_id FROM Player P1, Team_Member T \
                                WHERE P1.member_id = T.member_id \
                                AND T.name = '{player_name}');"
  data =  g.conn.execute(text(val))
  
  g.conn.commit()
  
  
  performancestats.append(f"{player_name}")
  for result in data.mappings():
  
    performancestats.append(f"season start date: {result['season_start_date']}")
    performancestats.append(f"goals scored: {result['nr_goals']}")
    performancestats.append(f"assists given: {result['nr_assists']}")
    performancestats.append(f"red cards received: {result['nr_red_cards']}")
    performancestats.append(f"yellow cards received: {result['nr_yellow_cards']}")
    performancestats.append(f"games started: {result['starting_xi']}")
    performancestats.append(f"games started: {result['nr_injuries']}") 
  data.close()
  
  val2 = f"SELECT T.team_name, P.player_type, M.age, M.height, M.weight \
  FROM Player P, Team_Member M, Team T \
  WHERE P.member_id = M.member_id AND T.team_id = M.team_id AND M.name = '{player_name}';"

  data =  g.conn.execute(text(val2))
  g.conn.commit()
  for result in data.mappings():
    performancestats.append(f"team name: {result['team_name']}")
    performancestats.append(f"position: {result['player_type']}")
    performancestats.append(f"age: {result['age']}")
    performancestats.append(f"height: {result['height']} m")
    performancestats.append(f"weight: {result['weight']} kg") 
  data.close()
  return jsonify({'performancestats': performancestats})
  
  
@players_bp.route('p/performancestats')
def returnplayerstats():
  
  return render_template("playerstats.html", player_stats=performancestats)


@players_bp.route('p/filteringlogic', methods=['POST'])
def filteringlogic():
  global filteredplayers
  filteredplayers = []
  args = request.get_json()
  attribute = args.get('arg1').lower()
  value = args.get('arg2')
  strval = ''
  if attribute == 'team':
    strval = f"SELECT TM.name AS player_name \
              FROM Team T \
              JOIN Team_Member TM ON T.team_id = TM.team_id \
              JOIN Player P ON TM.member_id = P.member_id \
              WHERE T.team_name = '{value}';"
  elif attribute == 'competition':
    strval = f"SELECT DISTINCT TM.name AS player_name \
    FROM Team_Member TM \
    JOIN Player P ON TM.member_id = P.member_id \
    JOIN Team T ON TM.team_id = T.team_id \
    JOIN contains C ON T.team_id = C.team_id \
    WHERE C.cname = '{value}';"
    
  elif attribute == 'position':
    strval = f"SELECT TM.name AS player_name \
              FROM Team_Member TM \
              JOIN Player P ON TM.member_id = P.member_id \
              WHERE P.player_type = '{value}';"


  data =  g.conn.execute(text(strval))    
  
  
  g.conn.commit()
  
  
  for result in data.mappings():
    filteredplayers.append(result['player_name'])
  data.close()
  return jsonify({'player': players})
 
@players_bp.route('p/filteredplayers')
def returnfilteredplayers():
  
  return render_template("filteredplayers.html", filtered_players=filteredplayers)

