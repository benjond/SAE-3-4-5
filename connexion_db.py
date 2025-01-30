from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

<<<<<<< Updated upstream
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        #
        db = g._database = pymysql.connect(
            host="serveurmysql.iut-bm.univ-fcomte.fr",
            # host="serveurmysql.iut-bm.univ-fcomte.fr",
            user="bjond",
            password="mdp",
            database="BDD_bjond",
=======
import os                                 # à ajouter
from dotenv import load_dotenv 
project_folder = os.path.expanduser('~/Documents/GitHub/SAE-3-4-5')  # adjust as appropriate (avec le dossier où se trouve le fichier .env et app.py)
load_dotenv(os.path.join(project_folder, '.env'))                          # à ajouter

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host=os.environ.get("HOST"),                # à modifier
            user=os.environ.get("LOGIN"),               # à modifier
            password=os.environ.get("PASSWORD"),        # à modifier
            database=os.environ.get("DATABASE"),        # à modifier
>>>>>>> Stashed changes
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        # à activer sur les machines personnelles :
        activate_db_options(db)
    return db

def activate_db_options(db):
    cursor = db.cursor()
    # Vérifier et activer l'option ONLY_FULL_GROUP_BY si nécessaire
    cursor.execute("SHOW VARIABLES LIKE 'sql_mode'")
    result = cursor.fetchone()
    if result:
        modes = result['Value'].split(',')
        if 'ONLY_FULL_GROUP_BY' not in modes:
            print('MYSQL : il manque le mode ONLY_FULL_GROUP_BY')   # mettre en commentaire
            cursor.execute("SET sql_mode=(SELECT CONCAT(@@sql_mode, ',ONLY_FULL_GROUP_BY'))")
            db.commit()
        else:
            print('MYSQL : mode ONLY_FULL_GROUP_BY  ok')   # mettre en commentaire
    # Vérifier et activer l'option lower_case_table_names si nécessaire
    cursor.execute("SHOW VARIABLES LIKE 'lower_case_table_names'")
    result = cursor.fetchone()
    if result:
        if result['Value'] != '0':
            print('MYSQL : valeur de la variable globale lower_case_table_names differente de 0')   # mettre en commentaire
            cursor.execute("SET GLOBAL lower_case_table_names = 0")
            db.commit()
        else :
            print('MYSQL : variable globale lower_case_table_names=0  ok')    # mettre en commentaire
    cursor.close()
