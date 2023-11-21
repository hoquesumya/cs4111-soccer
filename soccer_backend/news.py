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
news = []


news_bp = Blueprint("news_list", __name__, template_folder=tmpl_dir,static_folder='../static')



@news_bp.before_request
def before_request():

  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@news_bp.teardown_request
def teardown_request(exception):
  
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass
  



@news_bp.route('/newsquery')
def newssquery():
  global news
  news =  []
  data =  g.conn.execute(text("SELECT C.title, C.cname, C.news_type FROM competition_news C;"))
  
  g.conn.commit()
  
  
  for result in data.mappings():
      news.append([result['title'], result['cname'], result['news_type']])
  data.close()
  return news
  
  
  
@news_bp.route('/news')
def returnallnews():
  return render_template("news.html", all_news=news)

