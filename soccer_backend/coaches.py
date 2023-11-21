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
coaches = []


coaches_bp = Blueprint("coaches_list", __name__, template_folder=tmpl_dir,static_folder='../static')


@coaches_bp.before_request
def before_request():

  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@coaches_bp.teardown_request
def teardown_request(exception):
  
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass
  

@coaches_bp.route('/coachesquery')
def coachesquery():
  global coaches
  coaches =  []
  data =  g.conn.execute(text("SELECT TM.name, T.team_name, TM.age, TM.height, TM.weight, C.coach_type \
    FROM Team T, team_member TM, coach C \
    WHERE C.member_id = TM.member_id \
    AND T.team_id = TM.team_id;"))
  
  g.conn.commit()
  
  
  for result in data.mappings():
      coaches.append([result['name'], result['team_name'], result['age'], result['height'], result['weight'], result['coach_type']])
  data.close()
  return coaches
  
  
  
@coaches_bp.route('/coaches')
def returnallcoaches():
  return render_template("coaches.html", all_coaches=coaches)

