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
games = []


games_bp = Blueprint("games_list", __name__, template_folder=tmpl_dir,static_folder='../static')


@games_bp.before_request
def before_request():

  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@games_bp.teardown_request
def teardown_request(exception):
  
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass
  

@games_bp.route('/allgamesquery')
def allgamesquery():
  #games = []
  data =  g.conn.execute(text("""SELECT t1.team_name AS team1_name, g.final_score, t2.team_name AS team2_name, \
                              g.stoppage_time, g.game_date, g.location, g.cname \
  FROM Game AS g \
  JOIN matched AS m ON g.game_id = m.game_id \
  JOIN Team AS t1 ON m.team_id1 = t1.team_id \
  JOIN Team AS t2 ON m.team_id2 = t2.team_id; \
  """))
  
  g.conn.commit()
  for result in data.mappings():
        games.append([result['team1_name'], result['final_score'], result['team2_name'], 
                      result['stoppage_time'], result['game_date'], result['location'], result['cname']])
  data.close()
  return jsonify({'game': games})
  
  
  
@games_bp.route('/games')
def returnallgames():
  
  return render_template("games.html", all_games=games)
