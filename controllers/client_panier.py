#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = int(request.form.get('quantite'))

    sql = '''SELECT * FROM ligne_panier WHERE gant_id = %s AND utilisateur_id = %s'''
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    mycursor.execute("SELECT * FROM gant WHERE id_gant = %s", (id_article,))
    article = mycursor.fetchone()

    if article is None:
        flash("Article non trouvé", "error")
        return redirect('/client/article/show')

    if article['stock'] < quantite:
        flash("Stock insuffisant", "error")
        return redirect('/client/article/show')

    if article_panier:
        sql = "UPDATE ligne_panier SET quantite = quantite + %s WHERE utilisateur_id = %s AND gant_id = %s"
        mycursor.execute(sql, (quantite, id_client, id_article))
    else:
        sql = "INSERT INTO ligne_panier(utilisateur_id, gant_id, quantite, date_ajout) VALUES (%s, %s, %s, current_timestamp)"
        mycursor.execute(sql, (id_client, id_article, quantite))

    sql = "UPDATE gant SET stock = stock - %s WHERE id_gant = %s"
    mycursor.execute(sql, (quantite, id_article))

    get_db().commit()
    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', '')
    quantite = 1

    # Selection de la ligne du panier pour l'article et l'utilisateur connecté
    sql = '''SELECT * FROM ligne_panier WHERE gant_id = %s AND utilisateur_id = %s'''
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    if article_panier and article_panier['quantite'] > 1:
        # Mise à jour de la quantité dans le panier => -1 article
        sql = '''UPDATE ligne_panier SET quantite = quantite - %s WHERE utilisateur_id = %s AND gant_id = %s'''
        mycursor.execute(sql, (quantite, id_client, id_article))
    else:
        # Suppression de la ligne de panier
        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND gant_id = %s'''
        mycursor.execute(sql, (id_client, id_article))

    # Mise à jour du stock de l'article disponible
    sql = '''UPDATE gant SET stock = stock + %s WHERE id_gant = %s'''
    mycursor.execute(sql, (quantite, id_article))

    get_db().commit()
    return redirect('/client/article/show')





@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    
    # Sélection des lignes de panier pour l'utilisateur connecté
    sql = '''SELECT * FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql, (client_id,))
    items_panier = mycursor.fetchall()
    
    for item in items_panier:
        # Suppression de la ligne de panier de l'article pour l'utilisateur connecté
        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND gant_id = %s'''
        mycursor.execute(sql, (client_id, item['gant_id']))
        
        # Mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article
        sql2 = '''UPDATE gant SET stock = stock + %s WHERE id_gant = %s'''
        mycursor.execute(sql2, (item['quantite'], item['gant_id']))
    
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')

    # Sélection de la ligne du panier pour l'article et l'utilisateur connecté
    sql = '''SELECT * FROM ligne_panier WHERE gant_id = %s AND utilisateur_id = %s'''
    mycursor.execute(sql, (id_article, id_client))
    article_panier = mycursor.fetchone()

    if article_panier:
        # Suppression de la ligne de panier
        sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND gant_id = %s'''
        mycursor.execute(sql, (id_client, id_article))

        # Mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article
        sql2 = '''UPDATE gant SET stock = stock + %s WHERE id_gant = %s'''
        mycursor.execute(sql2, (article_panier['quantite'], id_article))

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    # test des variables puis
    # mise en session des variables
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/article/show')
