#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, session
from connexion_db import get_db

client_article = Blueprint('client_article', __name__, template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')
def client_article_show():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')

    condition_and = []
    list_param = []

    sql = '''SELECT gant.id_gant as id_article, gant.nom_gant as nom, gant.prix_gant as prix,
                    gant.stock as stock, gant.image as image, type_gant.nom_type_gant as type
             FROM gant
             JOIN type_gant ON gant.type_gant_id = type_gant.id_type_gant
             JOIN taille ON gant.taille_id = taille.id_taille'''

    if "filter_word" in session and session["filter_word"]:
        condition_and.append("gant.nom_gant LIKE %s")
        list_param.append(f"%{session['filter_word']}%")

    if "filter_prix_min" in session and session["filter_prix_min"]:
        condition_and.append("gant.prix_gant >= %s")
        list_param.append(session["filter_prix_min"])

    if "filter_prix_max" in session and session["filter_prix_max"]:
        condition_and.append("gant.prix_gant <= %s")
        list_param.append(session["filter_prix_max"])

    if "filter_types" in session and session["filter_types"]:
        placeholders = ', '.join(['%s'] * len(session["filter_types"]))
        condition_and.append(f"gant.type_gant_id IN ({placeholders})")
        list_param.extend(session["filter_types"])

    if condition_and:
        sql += " WHERE " + " AND ".join(condition_and)

    sql += " ORDER BY gant.nom_gant;"
    
    mycursor.execute(sql, tuple(list_param))
    articles = mycursor.fetchall()

    sql = '''SELECT id_type_gant as id_type_article, nom_type_gant AS libelle FROM type_gant ORDER BY nom_type_gant;'''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    sql = '''SELECT gant.id_gant as id_article, gant.nom_gant as nom, gant.prix_gant as prix,
                    gant.stock as stock, gant.image as image, ligne_panier.quantite as quantite
             FROM gant
             JOIN ligne_panier ON gant.id_gant = ligne_panier.gant_id
             WHERE ligne_panier.utilisateur_id = %s
             ORDER BY gant.nom_gant;'''
    
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()

    prix_total = None
    if articles_panier:
        sql = '''SELECT SUM(gant.prix_gant * ligne_panier.quantite) AS prix_total_panier 
                 FROM ligne_panier 
                 JOIN gant ON ligne_panier.gant_id = gant.id_gant
                 WHERE ligne_panier.utilisateur_id = %s;'''
        mycursor.execute(sql, (id_client,))
        prix_total = mycursor.fetchone()["prix_total_panier"]

    items_filtre = session.get('items_filtre', types_article)

    return render_template('client/boutique/panier_article.html',
                           articles=articles,
                           articles_panier=articles_panier,
                           prix_total=prix_total,
                           items_filtre=items_filtre)
