from flask import( Flask, request, render_template, g, redirect, 
                  Response, abort,jsonify,
                  make_response, Blueprint)
from config import engine
import requests
import os
from sqlalchemy import *
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool
basedir = os.path.abspath(os.path.dirname(__file__))
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates')
names = []

competitons= Blueprint("comp_list", __name__, static_folder=tmpl_dir,static_folder='../static')

@competitons.route("/comp_name")
def comp():
  data =  g.conn.execute(text("""SELECT * FROM competition"""))
  #names = []
  g.conn.commit()
  #results = cursor.mappings.all()
  for result in data.mappings():
    names.append(result["cname"])
  data.close()
  
  return jsonify({
    "name":names
  })
@competitons.route("/comp")
def temp():
  print(names)
  return render_template("competition.html", comp_name=names)



