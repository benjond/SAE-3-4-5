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

    mycursor = get_db().cursor()
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    print(f"filter_word : {filter_word}/{type(filter_word)}\nfilter_prix_min : {filter_prix_min}/{type(filter_prix_min)}\nfilter_prix_max : {filter_prix_max}/{type(filter_prix_max)}\nfilter_types : {filter_types}/{type(filter_types)}\n")

    # test des variables puis
    # mise en session des variables

    ## word :
    if filter_word:
        session['filter_word'] = filter_word
        sql1 = '''SELECT * FROM gant WHERE gant.nom_gant = %s'''
        mycursor.execute(sql1,filter_word)
        articles_filter = mycursor.fetchall()

    ## Prix :
    if filter_prix_max:
        session['filter_prix_max'] = filter_prix_max
        if not filter_prix_min:
            filter_prix_min = '0'
            session['filer_prix_min'] = filter_prix_min
        session['filter_prix_min'] = filter_prix_min
        sql2 = ''' SELECT * FROM gant WHERE gant.prix_gant BETWEEN %s and %s'''
        mycursor.execute(sql2,(filter_prix_min,filter_prix_max))
        articles_filter = mycursor.fetchall()

    ## types :
    if filter_types:
        sql3 = '''SELECT * FROM gant INNER JOIN type_gant ON type_gant.id_type_gant = gant.type_gant_id WHERE type_gant.id_type_gant IN (%s)''' % ','.join(['%s'] * len(filter_types))
        mycursor.execute(sql3, filter_types)
        articles_filter = mycursor.fetchall()

    # Mise à jour des lignes de panier en fonction des filtres
    session['articles_filter'] = articles_filter
    session['items_filtre'] = [item['id_gant'] for item in articles_filter]
    
    return redirect('/client/article/show')



@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    session.pop('articles_filter', None)
    session.pop('items_filtre', None)
    print("suppr filtre")
    return redirect('/client/article/show')
