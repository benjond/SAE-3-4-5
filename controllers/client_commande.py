#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, flash, session
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__, template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Fetch articles in the cart
    sql = '''
    SELECT gant.id_gant as id_article,
           gant.nom_gant as nom,
           gant.prix_gant as prix,
           gant.stock as stock,
           gant.image as image,
           ligne_panier.quantite as quantite
    FROM gant
    JOIN ligne_panier ON gant.id_gant = ligne_panier.gant_id
    WHERE ligne_panier.utilisateur_id = %s
    ORDER BY gant.nom_gant;
    '''
    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()

    if len(articles_panier) >= 1:
        # Fetch total price
        sql = '''
        SELECT SUM(gant.prix_gant * ligne_panier.quantite) as prix_total
        FROM gant
        JOIN ligne_panier ON gant.id_gant = ligne_panier.gant_id
        WHERE ligne_panier.utilisateur_id = %s
        '''
        mycursor.execute(sql, (id_client,))
        prix_total = mycursor.fetchone()['prix_total']
    else:
        prix_total = 0

    return render_template(
        'client/boutique/panier_validation_adresses.html',
        articles_panier=articles_panier,
        prix_total=prix_total,
        validation=1
    )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)
    id_client = session['id_user']

    # Fetch items in cart
    sql = '''
    SELECT gant.id_gant as id_article,
           gant.nom_gant as nom,
           gant.prix_gant as prix,
           gant.stock as stock,
           gant.image as image,
           ligne_panier.quantite as quantite
    FROM gant
    JOIN ligne_panier ON gant.id_gant = ligne_panier.gant_id
    WHERE ligne_panier.utilisateur_id = %s
    ORDER BY gant.nom_gant;
    '''
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    if not items_ligne_panier:
        flash(u'Pas d\'articles dans le panier', 'alert-warning')
        return redirect('/client/article/show')

    try:
        # Start transaction to insert order
        sql = '''
        INSERT INTO commande (date_achat, etat_id, utilisateur_id)
        SELECT %s, id_etat, %s FROM etat WHERE libelle_etat = 'En cours de préparation'
        '''
        mycursor.execute(sql, (datetime.now(), id_client))

        # Get last inserted order ID
        sql = '''SELECT last_insert_id() as last_insert_id'''
        mycursor.execute(sql)
        last_insert_id = mycursor.fetchone()['last_insert_id']

        # Insert items into the order line
        for item in items_ligne_panier:
            sql = '''DELETE FROM ligne_panier WHERE gant_id = %s AND utilisateur_id = %s'''
            mycursor.execute(sql, (item['id_article'], id_client))

            sql = '''INSERT INTO ligne_commande (commande_id, gant_id, quantite, prix)
                     VALUES (%s, %s, %s, %s)'''
            mycursor.execute(sql, (last_insert_id, item['id_article'], item['quantite'], item['prix']))

        get_db().commit()
        flash(u'Commande ajoutée', 'alert-success')
    except Exception as e:
        get_db().rollback()
        flash(u'Erreur lors de la commande: {}'.format(str(e)), 'alert-danger')

    return redirect('/client/article/show')


@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    # Fetch orders
    sql = '''
    SELECT commande.id_commande, commande.date_achat, etat.libelle_etat as libelle,
           SUM(ligne_commande.quantite * ligne_commande.prix) as prix_total,
           SUM(ligne_commande.quantite) as nbr_articles,
           commande.etat_id
    FROM commande
    JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
    JOIN etat ON commande.etat_id = etat.id_etat
    WHERE commande.utilisateur_id = %s
    GROUP BY commande.id_commande, commande.date_achat, etat.libelle_etat, commande.etat_id
    ORDER BY etat.libelle_etat, commande.date_achat DESC
    '''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    articles_commande = []
    commande_details = {}
    id_commande = request.args.get('id_commande', None)

    if id_commande:
        # Fetch articles in specific order
        sql = '''
        SELECT gant.nom_gant as nom,
               gant.prix_gant as prix,
               ligne_commande.quantite as quantite,
               (ligne_commande.quantite * gant.prix_gant) as prix_total
        FROM ligne_commande
        INNER JOIN gant ON ligne_commande.gant_id = gant.id_gant
        WHERE ligne_commande.commande_id = %s
        '''
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()

        # Fetch order details
        sql = '''
        SELECT commande.id_commande, commande.date_achat, etat.libelle_etat as etat,
               SUM(ligne_commande.quantite * ligne_commande.prix) as prix_total,
               SUM(ligne_commande.quantite) as nbr_articles
        FROM commande
        JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
        JOIN etat ON commande.etat_id = etat.id_etat
        WHERE commande.id_commande = %s
        GROUP BY commande.id_commande, etat.libelle_etat
        '''
        mycursor.execute(sql, (id_commande,))
        commande_details = mycursor.fetchone()

    return render_template(
        'client/commandes/show.html',
        commandes=commandes,
        articles_commande=articles_commande,
        commande_details=commande_details
    )