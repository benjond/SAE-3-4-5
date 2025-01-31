#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, flash, session
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                            template_folder='templates')


# validation de la commande : partie 2 -- vue pour choisir les adresses (livraision et facturation)
@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''SELECT gant.id_gant as id_article,
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
    # etape 2 : selection des adresses
    return render_template('client/boutique/panier_validation_adresses.html'
                           #, adresses=adresses
                           , articles_panier=articles_panier
                           , prix_total= prix_total
                           , validation=1
                           #, id_adresse_fav=id_adresse_fav
                           )


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()

    # choix de(s) (l')adresse(s)

    id_client = session['id_user']
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
        ORDER BY gant.nom_gant;'''
    mycursor.execute(sql, (id_client,))
    items_ligne_panier = mycursor.fetchall()
    if items_ligne_panier is None or len(items_ligne_panier) < 1:
        flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
        return redirect('/client/article/show')
    # if items_ligne_panier is None or len(items_ligne_panier) < 1:
    #     flash(u'Pas d\'articles dans le ligne_panier', 'alert-warning')
    #     return redirect('/client/article/show')
    # https://pynative.com/python-mysql-transaction-management-using-commit-rollback/
    #a = datetime.strptime('my date', "%b %d %Y %H:%M")

    sql = '''
    INSERT INTO commande (date_achat, etat_id, utilisateur_id)
    VALUES (%s, (SELECT id_etat FROM etat WHERE libelle_etat = %s), %s)'''
    mycursor.execute(sql, (datetime.now(), 'en attente', id_client))

    sql = '''SELECT last_insert_id() as last_insert_id'''
    mycursor.execute(sql)
    last_insert_id = mycursor.fetchone()['last_insert_id']
    # numéro de la dernière commande
    for item in items_ligne_panier:
        sql = '''DELETE FROM ligne_panier WHERE gant_id = %s AND utilisateur_id = %s'''
        mycursor.execute(sql, (item['id_article'], id_client))

        sql = '''INSERT INTO ligne_commande (commande_id, gant_id, quantite, prix)
             VALUES (%s, %s, %s, %s)'''
        mycursor.execute(sql, (last_insert_id, item['id_article'], item['quantite'], item['prix']))

    get_db().commit()
    flash(u'Commande ajoutée','alert-success')
    return redirect('/client/article/show')




@client_commande.route('/client/commande/show', methods=['get','post'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    sql = '''
    SELECT commande.id_commande, commande.date_achat, etat.libelle_etat as libelle,
           SUM(ligne_commande.quantite * ligne_commande.prix) as prix_total,
           SUM(ligne_commande.quantite) as nbr_articles
    FROM commande
    JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
    JOIN etat ON commande.etat_id = etat.id_etat
    WHERE commande.utilisateur_id = %s
    GROUP BY commande.id_commande, etat.libelle_etat
    ORDER BY etat.libelle_etat, commande.date_achat DESC
    '''
    mycursor.execute(sql, (id_client,))
    commandes = mycursor.fetchall()


    articles_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    if id_commande != None:
        print(id_commande)
        # partie 1 : sélection du détail d'une commande
        sql = '''
        SELECT gant.nom_gant as nom,
               gant.prix_gant as prix,
               ligne_commande.quantite as quantite,
               ligne_commande.prix as prix_total
        FROM ligne_commande
        INNER JOIN gant ON ligne_commande.gant_id = gant.id_gant
        WHERE ligne_commande.commande_id = %s
        '''
        mycursor.execute(sql, (id_commande,))
        articles_commande = mycursor.fetchall()

        # partie 2 : sélection de l'adresse de livraison et de facturation de la commande sélectionnée
        sql = '''
        SELECT adresse.ligne1, adresse.ligne2, adresse.ville, adresse.code_postal, adresse.pays
        FROM adresse
        INNER JOIN commande_adresse ON adresse.id_adresse = commande_adresse.adresse_id
        WHERE commande_adresse.commande_id = %s
        '''
        mycursor.execute(sql, (id_commande,))
        commande_adresses = mycursor.fetchall()

    return render_template('client/commandes/show.html'
                           , commandes=commandes
                           , articles_commande=articles_commande
                           , commande_adresses=commande_adresses
                           )