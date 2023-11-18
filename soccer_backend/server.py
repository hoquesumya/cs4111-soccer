
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, abort,jsonify
from config import engine
basedir = os.path.abspath(os.path.dirname(__file__))
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
print(tmpl_dir)
app = Flask(__name__, template_folder=tmpl_dir, static_folder='../static')


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
  
  #context = dict(data = names)
  #return render_template("index.html", **context)
  return render_template("home.html")



@app.route('/competition')
def comp():
  data =  g.conn.execute(text("""SELECT * FROM competition"""))
  names = []
  g.conn.commit()
  #results = cursor.mappings.all()
  for result in data.mappings():
    names.append(result["cname"])
  data.close()

  return jsonify({
    "name": names
  })
@app.route('/comp')
def temp():
  return render_template("competition.html")

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
