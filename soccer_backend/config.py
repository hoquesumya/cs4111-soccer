import os
from dotenv import load_dotenv
from sqlalchemy import *
from flask import( Flask, request, render_template, g, redirect, 
                  Response, abort,jsonify,
                  make_response, Blueprint)

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,".env"))

DATABASEURI = os.getenv("DATABASEURI")
engine = create_engine(DATABASEURI)

#zconnection = engine.connect()

