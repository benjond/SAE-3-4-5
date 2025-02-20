#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, flash, session
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__, template_folder='templates')

@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql = '''
    SELECT commande.id_commande, commande.date_achat, etat.libelle_etat as libelle,
           SUM(ligne_commande.quantite * ligne_commande.prix) as prix_total,
           SUM(ligne_commande.quantite) as nbr_articles,
           commande.etat_id
    FROM commande
    JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
    JOIN etat ON commande.etat_id = etat.id_etat
    WHERE commande.utilisateur_id = %s
    GROUP BY commande.id_commande, etat.libelle_etat, commande.etat_id
    ORDER BY etat.libelle_etat, commande.date_achat DESC
    '''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()

    articles_commande = []
    commande_adresses = {}
    commande_details = {}
    id_commande = request.args.get('id_commande', None)

    if id_commande:
        sql = '''
        SELECT gant.nom_gant as nom,
               gant.prix_gant as prix,
               ligne_commande.quantite as quantite,
               (ligne_commande.quantite * ligne_commande.prix) as prix_total
        FROM ligne_commande
        INNER JOIN gant ON ligne_commande.gant_id = gant.id_gant
        WHERE ligne_commande.commande_id = %s
        '''
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()

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
        commande_adresses=commande_adresses,
        commande_details=commande_details
    )
