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
team_id=[]
team_names = []
nr_total_players = []
nr_total_coaches = []


teams= Blueprint("team", __name__, template_folder=tmpl_dir,static_folder='../static')

@teams.before_request
def before_request():

  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@teams.teardown_request
def teardown_request(exception):

  try:
    g.conn.close()
  except Exception as e:
    pass
  
@teams.route('/')
def index():
  return jsonify({
    "hello":"hello"
  })

@teams.route('/team-info')
def team():
  data =  g.conn.execute(text("""SELECT * FROM team"""))
  g.conn.commit()
  #results = cursor.mappings.all()
  for result in data.mappings():
    team_id.append(result["team_id"])
    team_names.append(result["team_name"])
    nr_total_coaches.append(result["nr_total_coaches"])
    nr_total_players.append(result['nr_total_players'])

  data.close()
  
  return jsonify({
    "name":team_names
  })

@teams.route('/teams')
def temp():
  team_info ={
    "id":team_id,
     "team_name":team_names,
     "total_players":nr_total_players,
     "total_coaches":nr_total_coaches

  }
  return render_template("teams.html", teams_info=team_info)
