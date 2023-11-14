import os
from dotenv import load_dotenv
from sqlalchemy import *

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,".env"))

DATABASEURI = os.getenv("DATABASEURI")
engine = create_engine(DATABASEURI)
