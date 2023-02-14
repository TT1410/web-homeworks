from mongoengine import connect
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('MONGO_DB', 'user')
mongodb_pass = config.get('MONGO_DB', 'password')
db_name = config.get('MONGO_DB', 'db_name')
domain = config.get('MONGO_DB', 'host')


URI = (f"mongodb://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?"
       "ssl=true&replicaSet=atlas-lhkelk-shard-0&authSource=admin&retryWrites=true&w=majority")

# connect to cluster on AtlasDB with connection string
connect(host=URI, ssl=True)
