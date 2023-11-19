
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, abort,jsonify,make_response
from config import engine
import requests
basedir = os.path.abspath(os.path.dirname(__file__))
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
print(tmpl_dir)


app = Flask(__name__, template_folder=tmpl_dir, static_folder='../static')
names = []
games = []
players = []
performancestats = []

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def index():

  print(request.args)
  return render_template("home.html")



@app.route('/competition')
def comp():
  data =  g.conn.execute(text("""SELECT * FROM competition"""))
  g.conn.commit()
  for result in data.mappings():
    if result["cname"] not in names: names.append(result["cname"])
  data.close()
  
  return jsonify({
    "name":names
  })
  
@app.route('/comp')
def temp():
  print(names)
  return render_template("competition.html", comp_name=names)

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.json['name']
  print(name)
  params_dict = {"name":name}
  g.conn.execute(text('INSERT INTO test(name) VALUES (:name)'), params_dict)
  g.conn.commit()
  return jsonify({
            "name":name
        }),200
  
  #return redirect('/')

@app.route('/allgamesquery')
def allgamesquery():
  #games = []
  data =  g.conn.execute(text("""SELECT t1.team_name AS team1_name, g.final_score, t2.team_name AS team2_name
  FROM Game AS g
  JOIN matched AS m ON g.game_id = m.game_id
  JOIN Team AS t1 ON m.team_id1 = t1.team_id
  JOIN Team AS t2 ON m.team_id2 = t2.team_id;
  """))
  
  g.conn.commit()
  print(data.mappings())
  for result in data.mappings():
    val = f"{result['team1_name']} {result['final_score']} {result['team2_name']}"
    if val not in games: games.append(val)
  data.close()
  return jsonify({'game': games})
  #return render_template("games.html", all_games=jsonify({'game': games}))
  
  
@app.route('/games')
def returnallgames():
  #print(games)
  return render_template("games.html", all_games=games)


@app.route('/allplayersquery')
def allplayersquery():
  
  data =  g.conn.execute(text("""SELECT T.name FROM Player P, Team_Member T WHERE P.member_id = T.member_id;"""))
  
  g.conn.commit()
  
  #print(data.mappings())
  for result in data.mappings():
    if result['name'] not in players: players.append(result['name'])
  data.close()
  return jsonify({'player': players})
  
  
@app.route('/players')
def returnallplayers():
  return render_template("players.html", all_players=players)


@app.route('/playerstats', methods=['POST'])
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
  
  #print(data.mappings())
  for result in data.mappings():
    print(result)
    performancestats.append(f"season start date: {result['season_start_date']}")
    performancestats.append(f"goals scored: {result['nr_goals']}")
    performancestats.append(f"assists given: {result['nr_assists']}")
    performancestats.append(f"red cards received: {result['nr_red_cards']}")
    performancestats.append(f"yellow cards received: {result['nr_yellow_cards']}")
    performancestats.append(f"games started: {result['starting_xi']}")
    performancestats.append(f"games started: {result['nr_injuries']}") 
  data.close()
  #print(performancestats)
  val2 = f"SELECT T.team_name, P.player_type, M.age, M.height, M.weight \
  FROM Player P, Team_Member M, Team T \
  WHERE P.member_id = M.member_id AND T.team_id = M.team_id AND M.name = '{player_name}';"

  data =  g.conn.execute(text(val2))
  g.conn.commit()
  for result in data.mappings():
    performancestats.append(f"team name: {result['team_name']}")
    performancestats.append(f"position: {result['player_type']}")
    performancestats.append(f"age: {result['age']}")
    performancestats.append(f"height: {result['height']}")
    performancestats.append(f"weight: {result['weight']}") 
  data.close()
  return jsonify({'performancestats': performancestats})
  
  
@app.route('/performancestats')
def returnplayerstats():
  #print(performancestats)
  return render_template("playerstats.html", player_stats=performancestats)




if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
  

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()
