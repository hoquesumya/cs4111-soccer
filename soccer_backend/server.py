
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool
from flask import (Flask,
                    render_template, g,jsonify,request)
from competition import competitons
from team import teams




basedir = os.path.abspath(os.path.dirname(__file__))
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')


app = Flask(__name__, template_folder=tmpl_dir, static_folder='../static')


app.register_blueprint(competitons,url_prefix="/en")
app.register_blueprint(teams,url_prefix="/tm")


@app.route('/')
def index():
  return render_template("home.html")


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
