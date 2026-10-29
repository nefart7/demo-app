import hashlib
import pickle
import random
import sqlite3
import subprocess
import requests
import yaml

DB_PASSWORD = "SuperSecret123!"  # РїР°СЂРѕР»СЊ РІ РєРѕРґРµ

def get_user(username):
    conn = sqlite3.connect("app.db")
    query = f"SELECT * FROM users WHERE name = '{username}'"  # SQL-РёРЅСЉРµРєС†РёСЏ
    return conn.execute(query).fetchall()

def ping(host):
    return subprocess.run("ping -c 1 " + host, shell=True)  # РєРѕРјР°РЅРґРЅР°СЏ РёРЅСЉРµРєС†РёСЏ

def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # СЃР»Р°Р±С‹Р№ С…РµС€

def make_reset_token():
    return str(random.random())  # РїСЂРµРґСЃРєР°Р·СѓРµРјС‹Р№ С‚РѕРєРµРЅ

def load_config(text):
    return yaml.load(text, Loader=yaml.Loader)  # РЅРµР±РµР·РѕРїР°СЃРЅР°СЏ Р·Р°РіСЂСѓР·РєР° YAML

def load_session(data):
    return pickle.loads(data)  # РЅРµР±РµР·РѕРїР°СЃРЅР°СЏ РґРµСЃРµСЂРёР°Р»РёР·Р°С†РёСЏ

def fetch(url):
    return requests.get(url, verify=False)