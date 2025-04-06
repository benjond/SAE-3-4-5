#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                        template_folder='templates')


@client_commentaire.route('/client/article/details', methods=['GET'])
def client_article_details():
    
    ## TODO : Définir et Remplir les base de données 'commandes_articles' et 'nb_commentaire'
    ## Attention, nb_commentaire doit avoir nb_commentaire_utilisateur et nb_commentaire_total
    ## Et commandes_articles doit avec nb_commandes_article

    ## partie 4
    # client_historique_add(id_article, id_client)
    # D'apres 'article_details.html' commandes_articles.nb_commandes_article , 
    # nb_commentaires.nb_commentaires_utilisateur doivent etre defini dans la BDD.
    # Ainsi que pour les notes de meme avec commandes_articles.nb_commandes_article 

    # init variables
    ## Il faut que cela soit des dictionnaires.
    article=[]
    commandes_articles=[]
    nb_commentaires=[] 
    
    mycursor = get_db().cursor()
    id_article =  request.args.get('id_article', None)
    id_client = session['id_user']
    
    ## Gant (ok)
    sql = '''
        SELECT id_gant as id_article, nom_gant, poids, couleur, prix_gant, description, taille_id, type_gant_id , fournisseur , marque, stock, nb_notes, moyenne_notes_gant, image 
        FROM gant 
        WHERE id_gant = %s
    '''
    mycursor.execute(sql, id_article)
    article = mycursor.fetchone()
    if article is None:
        abort(404, "pb id article")
    
    ## Commentaire
    # Affiché en ordre Chronologique
    sql = '''
        SELECT commentaire_gant.commentaire,commentaire_gant.gant_id,commentaire_gant.utilisateur_id, commentaire_gant.date_redaction,note_gant.note, utilisateur.nom
        FROM commentaire_gant
        INNER JOIN note_gant ON commentaire_gant.utilisateur_id = note_gant.utilisateur_id AND commentaire_gant.gant_id = note_gant.gant_id
        INNER JOIN utilisateur ON commentaire_gant.utilisateur_id = utilisateur.id_utilisateur
        WHERE commentaire_gant.gant_id = %s
        ORDER BY commentaire_gant.date_redaction ASC
    '''
    mycursor.execute(sql, (id_article))
    commentaires = mycursor.fetchall()
    print(commentaires)
    
    
    ## Commande Article
    # Si la commande et défini et que l'article dont l'on veut mettre un avis dessus
    # et dans la liste de commande alors l'on incrémente le nombre de commandes articles
    sql = '''
        SELECT COUNT(*) AS nb_commandes_article
        FROM commande
        INNER JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
        WHERE commande.utilisateur_id = %s AND ligne_commande.gant_id = %s
    '''
    mycursor.execute(sql, (id_client, id_article))
    commandes_articles = mycursor.fetchone()
    print(commandes_articles)

    
    ## Note (presque ok)
    sql = '''
        SELECT note
        FROM note_gant
        WHERE utilisateur_id = %s AND gant_id=%s
    '''
    mycursor.execute(sql, (id_client, id_article))
    note = mycursor.fetchone()
    print('note',note)
    if note:
        note=note['note']

    ## Nombre Commentaire

    sql = '''
        SELECT 
            COUNT(
                CASE WHEN utilisateur_id = %s THEN 1 END
            ) AS nb_commentaires_utilisateur,
            COUNT(
                CASE WHEN utilisateur_id = %s AND valider = 1 THEN 1 END
            ) AS nb_commentaires_utilisateur_valide,
            COUNT(
                CASE WHEN valider = 1 THEN 1 END
            ) AS nb_commentaires_total_valide,
            COUNT(*) AS nb_commentaires_total
        FROM commentaire_gant
        WHERE gant_id = %s
    '''
    mycursor.execute(sql, (id_client,id_client, id_article))
    nb_commentaires = mycursor.fetchone()


    ## Moyen Note (a l'air d'etre ok)
    # On update la base de données de gant et comme voulu l'on fait les calcules
    # de moyennes et de total avec SQL et non PYTHON.

    sql = '''
        UPDATE gant
        SET moyenne_notes_gant = (
            SELECT CASE 
                WHEN (SUM(note) DIV COUNT(DISTINCT note)) = 0 THEN NULL
                ELSE SUM(note) DIV COUNT(DISTINCT note)
            END
            FROM note_gant
            WHERE gant_id = %s
        ),
        nb_notes = (
            SELECT COUNT(note)
            FROM note_gant
            WHERE gant_id = %s
        )
        WHERE id_gant = %s
    '''
    mycursor.execute(sql , (id_article, id_article, id_article))
    # moyenne_notes = mycursor.fetchone()
    # if moyenne_notes = 0 : moyenne_notes = None
    get_db().commit()

    return render_template('client/article_info/article_details.html'
                           , article=article
                           , commentaires=commentaires
                           , commandes_articles=commandes_articles
                           , note=note
                            , nb_commentaires=nb_commentaires
                           )



@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    ## TODO : Debugger la fonction
    ## PROBLEME = id_client, id_article et commentaire sont null.

    commentaire = request.form.get('commentaire', None) # !
    id_client = session['id_user'] # !
    id_article = request.form.get('id_article', None) # !

    ## Vérification d'achat
    # On fait une jointure pour savoir si dans les tables commande et
    # ligne_commande l'utilisateur a bien commander le gant
    sql = '''
        SELECT COUNT(*) AS nb_commandes
        FROM commande
        INNER JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
        WHERE commande.utilisateur_id = %s AND ligne_commande.gant_id = %s
    '''
    mycursor.execute(sql, (id_client, id_article))
    result = mycursor.fetchone()

    if result['nb_commandes'] == 0:
        flash(u'Vous ne pouvez commenter que les articles que vous avez achetés.', 'alert-warning')
        return redirect('/client/article/details?id_article=' + id_article)


    ## Rédaction Commentaire + Vérification du commentaire
    if commentaire == '':
        flash(u'Commentaire non prise en compte')
        return redirect('/client/article/details?id_article='+id_article)
    if commentaire != None and len(commentaire)>0 and len(commentaire) <3 :
        flash(u'Commentaire avec plus de 2 caractères','alert-warning')              # 
        return redirect('/client/article/details?id_article='+id_article)

    tuple_insert = (commentaire, id_client, id_article)
    print(tuple_insert)
    
    ## Source : https://mariadb.com/kb/en/now/
    # À voir comment formater la date.
    sql = '''
        INSERT INTO commentaire_gant (commentaire_gant_id,commentaire, utilisateur_id, gant_id, date_redaction)
        VALUES (NULL,%s, %s, %s, NOW())
    '''
    
    mycursor.execute(sql, tuple_insert)
    
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_detete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_redaction', None) ## À voir avec le formatage
    print("date:",date_publication)
    sql = '''
        DELETE FROM commentaire_gant
        WHERE utilisateur_id = %s AND gant_id = %s AND date_redaction = %s
    '''
    tuple_delete=(id_client,id_article,date_publication)
    mycursor.execute(sql, tuple_delete)
    
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_article = request.form.get('id_article', None)
    tuple_insert = (note, id_client, id_article)
    print(tuple_insert)
    
    sql = '''
        INSERT INTO note_gant (note_gant_id,note, utilisateur_id, gant_id)
        VALUES (NULL,%s, %s, %s)
    '''
    mycursor.execute(sql, tuple_insert)
    
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_article = request.form.get('id_article', None)
    tuple_update = (note, id_client, id_article)
    print(tuple_update)
    
    sql = '''  
        UPDATE note_gant
        SET note = %s
        WHERE utilisateur_id = %s AND gant_id = %s
    '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)

@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', None)
    tuple_delete = (id_client, id_article)
    print(tuple_delete)
    
    sql = '''  
        DELETE FROM note_gant
        WHERE utilisateur_id = %s AND gant_id = %s
    '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?id_article='+id_article)
