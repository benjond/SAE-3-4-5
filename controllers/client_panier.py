#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, flash, session
from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__, template_folder='templates')

@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')
    id_article = request.form.get('id_article')
    quantite = int(request.form.get('quantite'))

    sql = '''SELECT stock FROM gant WHERE id_gant = %s'''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()

    if not article:
        flash("Article non trouvé", "error")
        return redirect('/client/article/show')

    if article['stock'] < quantite:
        flash("Stock insuffisant", "error")
        return redirect('/client/article/show')

    sql = '''SELECT quantite FROM ligne_panier WHERE utilisateur_id = %s AND gant_id = %s'''
    mycursor.execute(sql, (id_client, id_article))
    existing_item = mycursor.fetchone()

    if existing_item:
        sql = '''UPDATE ligne_panier SET quantite = quantite + %s WHERE utilisateur_id = %s AND gant_id = %s'''
        mycursor.execute(sql, (quantite, id_client, id_article))
    else:
        sql = '''INSERT INTO ligne_panier(utilisateur_id, gant_id, quantite, date_ajout) 
                 VALUES (%s, %s, %s, current_timestamp)'''
        mycursor.execute(sql, (id_client, id_article, quantite))

    sql = "UPDATE gant SET stock = stock - %s WHERE id_gant = %s"
    mycursor.execute(sql, (quantite, id_article))

    get_db().commit()
    return redirect('/client/article/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')
    id_article = request.form.get('id_article')
    
    sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND gant_id = %s'''
    mycursor.execute(sql, (id_client, id_article))

    sql = '''UPDATE gant SET stock = stock + %s WHERE id_gant = %s'''
    mycursor.execute(sql, (1, id_article))

    get_db().commit()
    return redirect('/client/article/show')

@client_panier.route('/client/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')
    id_article = request.form.get('id_article')
    quantite = int(request.form.get('quantite'))

    sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s AND gant_id = %s'''
    mycursor.execute(sql, (id_client, id_article))

    sql = '''UPDATE gant SET stock = stock + %s WHERE id_gant = %s'''
    mycursor.execute(sql, (quantite, id_article))

    get_db().commit()
    return redirect('/client/article/show')

@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')

    sql = '''SELECT gant_id, quantite FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))
    items_panier = mycursor.fetchall()

    for item in items_panier:
        sql = '''UPDATE gant SET stock = stock + %s WHERE id_gant = %s'''
        mycursor.execute(sql, (item['quantite'], item['gant_id']))

    sql = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql, (id_client,))

    get_db().commit()
    return redirect('/client/article/show')

@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    session['filter_word'] = request.form.get('filter_word', '').strip() or ''
    session['filter_prix_min'] = request.form.get('filter_prix_min', '').strip() or ''
    session['filter_prix_max'] = request.form.get('filter_prix_max', '').strip() or ''
    session['filter_types'] = request.form.getlist('filter_types') or ''
    return redirect('/client/article/show')

@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    session.pop('articles_filter', None)
    session.pop('items_filtre', None)
    return redirect('/client/article/show')
