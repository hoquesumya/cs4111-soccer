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

names = []
comp_date=[]


competitons= Blueprint("comp_list", __name__, template_folder=tmpl_dir,static_folder='../static')

@competitons.before_request
def before_request():

  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@competitons.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass




@competitons.route('/competition')
def comp():
  #filter some of the data out because whe don't have any entry of that particular row
  global names
  global comp_date
  names=[]
  comp_date=[]
  data =  g.conn.execute(text("""SELECT DISTINCT * FROM competition C
                              WHERE C.cname !='UEFA Champions League' 
                              AND C.cname !='Serie A'
                               AND C.start_date !='2022-08-06'
                              
                              """))
  g.conn.commit()
  #results = cursor.mappings.all()
  for result in data.mappings():
    names.append(result["cname"])
    start_date = result["start_date"].strftime('%Y/%m/%d')
    end_date = result["end_date"].strftime('%Y/%m/%d')

    comp_date.append([start_date,end_date])

    
  data.close()
  
  return jsonify({
    "name":names
  })
  
@competitons.route('/comp')
def temp():
  comp_info ={
    "name":names,
     "date":comp_date
  }
  return render_template("competition.html", comp_info=comp_info)




@competitons.route('/competition-sql-query',methods=['POST'])
def select_query():
  query_text=""
  query_result=[]
  game_id=[]
  game_location=[]
  game_date=[]
  query_type=request.json['type']
  comp_name = request.json['comp-name']
  start_date = request.json['start-date']
  end_date = request.json['end-date']
  temp_startDate= datetime.datetime.strptime(start_date,"%Y/%m/%d")
  temp_endDate= datetime.datetime.strptime(end_date,"%Y/%m/%d")
  startDate = datetime.date(temp_startDate.year, temp_startDate.month, temp_startDate.day)
  endDate = datetime.date(temp_endDate.year, temp_endDate.month, temp_endDate.day)

  params_dict = {"comp_name":comp_name,
                 "start_date":startDate
               }
  if (query_type==0):
    query_text= """SELECT T.team_name 
                              FROM team T, contains C
                              WHERE T.team_id=C.team_id AND C.cname= :comp_name 
                              AND C.start_date=:start_date
                              
                              """
  elif query_type==1:
    query_text = """SELECT T.name 
                    FROM Team_Member T, Player P 
                    WHERE T.member_id=P.member_id  AND T.team_id IN(SELECT T1.team_id
                                                                    FROM team T1, contains C
                                                                    WHERE T1.team_id=C.team_id 
                                                                    AND C.cname =:comp_name 
                                                                    AND C.start_date=:start_date)
                  """
  else:
    query_text1 = """
          SELECT DISTINCT g.game_id, g.location, g.game_date 
          FROM matched M,game g WHERE g.game_id = M.game_id 
          AND M.team_id1 IN  (SELECT T1.team_id
                              FROM team T1, contains C
                               WHERE T1.team_id=C.team_id 
                                AND C.cname =:comp_name 
                                AND C.start_date=:start_date) 
           OR M.team_id2 IN (SELECT T2.team_id
                               FROM team T2, contains C
                               WHERE T2.team_id=C.team_id 
                                AND C.cname =:comp_name 
                                AND C.start_date=:start_date);


                """
    query_text="""SELECT * FROM game g WHERE g.cname =:comp_name AND g.game_date >:start_date;

                
          """
  
  data =  g.conn.execute(text(query_text),params_dict)
  g.conn.commit()
  for res in data.mappings():
    if query_type==0:
      query_result.append(res['team_name'])
    elif query_type==1:
      query_result.append(res['name'])
    else:

      game_id.append(res["game_id"])
      game_location.append(res["location"])
      game_date.append(res["game_date"].strftime('%Y/%m/%d'))

  
  data.close()

  if query_type==1 or query_type==0:
      return jsonify({
        "query_result":query_result
      },200)
  else:
    
    return jsonify({
      "game_id":game_id,
      "game_location":game_location,
      "game_date":game_date
    })


