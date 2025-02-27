#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, session

from connexion_db import get_db

client_article = Blueprint('client_article', __name__,
                        template_folder='templates')

@client_article.route('/client/index')
@client_article.route('/client/article/show')              # remplace /client
def client_article_show():                                 # remplace client_index
    mycursor = get_db().cursor()
    id_client = session['id_user']
    list_param = []
    condition_and = ""
    if 'filtre_nom' in request.args:
        filtre_nom = request.args['filtre_nom']
        condition_and += " AND nom_gant LIKE %s"
        list_param.append(f"%{filtre_nom}%")
    # utilisation du filtre
    # prise en compte des commentaires et des notes dans le SQL
    sql = ''' SELECT id_gant as id_article
                    , nom_gant as nom
                    , prix_gant as prix
                    , stock as stock
                    , image as image
                FROM gant
                ORDER BY nom_gant;
            '''
    mycursor.execute(sql)
    gant = mycursor.fetchall()
    articles = gant
            

    # pour le filtre
    sql = '''SELECT id_type_gant as id_type_article, nom_type_gant AS libelle FROM type_gant ORDER BY nom_type_gant;'''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()
        


    # pour le panier
    sql = '''SELECT gant.id_gant as id_article
                    , gant.nom_gant as nom
                    , gant.prix_gant as prix
                    , gant.stock as stock
                    , gant.image as image
                    , ligne_panier.quantite as quantite
                FROM gant
                JOIN ligne_panier ON gant.id_gant = ligne_panier.gant_id
                WHERE ligne_panier.utilisateur_id = %s
                ORDER BY gant.nom_gant;
    '''

    mycursor.execute(sql, (id_client,))
    articles_panier = mycursor.fetchall()

    prix_total = None
    if len(articles_panier) >= 1:
        # calcul du prix total du panier
        pass

    # utilise les articles filtées de la session si il sont disponible
    if 'articles_filter' in session and session['articles_filter']:
        articles = session['articles_filter']
        items_filtre = session.get('items_filtre') or []
    else:
        items_filtre = types_article

    return render_template('client/boutique/panier_article.html'
                           , articles=articles
                           , articles_panier=articles_panier
                           , prix_total=prix_total
                           , items_filtre=items_filtre
                           )
