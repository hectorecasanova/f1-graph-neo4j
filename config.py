from decouple import config
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

NEO4J_URI = config("NEO4J_URI")
NEO4J_USERNAME = config("NEO4J_USERNAME")
NEO4J_PASSWORD = config("NEO4J_PASSWORD")
AURA_INSTANCEID = config("AURA_INSTANCEID")
AURA_INSTANCENAME = config("AURA_INSTANCENAME")
