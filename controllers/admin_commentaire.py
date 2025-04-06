#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                        template_folder='templates')


@admin_commentaire.route('/admin/article/commentaires', methods=['GET'])
def admin_article_details():
    mycursor = get_db().cursor()
    id_article =  request.args.get('id_article', None)
    
    ## Commentaire
    sql = '''
        SELECT commentaire_gant.commentaire,commentaire_gant.gant_id,commentaire_gant.utilisateur_id, commentaire_gant.date_redaction,note_gant.note, utilisateur.nom
        FROM commentaire_gant
        INNER JOIN note_gant ON commentaire_gant.utilisateur_id = note_gant.utilisateur_id AND commentaire_gant.gant_id = note_gant.gant_id
        INNER JOIN utilisateur ON commentaire_gant.utilisateur_id = utilisateur.id_utilisateur
        WHERE commentaire_gant.gant_id = %s
        ORDER BY commentaire_gant.date_redaction ASC
    ''' ## gant_id ne marche pas, TODO : trouver la cause du probleme
    mycursor.execute(sql, (id_article))    
    commentaires = {}
    commentaires = mycursor.fetchone()


    ## Article
    sql = '''
        SELECT *
        FROM gant
        WHERE id_gant = %s
    '''
    mycursor.execute(sql,(id_article))
    article = []
    article = mycursor.fetchone()


    ## Nombre de commentaires
    sql = '''
        SELECT 
            COUNT(*) AS nb_commentaires_total,
            COUNT(CASE WHEN valider = 1 THEN 1 END) AS nb_commentaires_valider
        FROM commentaire_gant
        WHERE gant_id = %s
    '''
    mycursor.execute(sql,(id_article))
    nb_commentaires = []
    nb_commentaires = mycursor.fetchone()

    return render_template('admin/article/show_article_commentaires.html'
                           , commentaires=commentaires
                           , article=article
                           , nb_commentaires=nb_commentaires
                           )

@admin_commentaire.route('/admin/article/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    
    sql = '''
        DELETE FROM commentaire_gant
        WHERE utilisateur_id = %s AND gant_id = %s AND date_redaction = %s
    '''

    tuple_delete=(id_utilisateur,id_article,date_publication)
    mycursor.execute(sql,tuple_delete)
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)


@admin_commentaire.route('/admin/article/commentaires/repondre', methods=['POST','GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        id_article = request.args.get('id_article', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/article/add_commentaire.html',id_utilisateur=id_utilisateur,id_article=id_article,date_publication=date_publication )

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']   #1 admin
    id_article = request.form.get('id_article', None)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''
        INSERT INTO commentaire_gant (commentaire_gant_id, commentaire, utilisateur_id , date_redaction)
        VALUES (NULL,%s,%s,%s,NOW())
    '''
    tuple_insert = (commentaire , id_utilisateur , id_article)
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)


@admin_commentaire.route('/admin/article/commentaires/valider', methods=['POST','GET'])
def admin_comment_valider():
    id_article = request.args.get('id_article', None)
    mycursor = get_db().cursor()
    sql = '''
        UPDATE commentaire_gant
        SET valider = TRUE
        WHERE gant_id = %s
    '''
    mycursor.execute(sql, id_article)
    get_db().commit()
    return redirect('/admin/article/commentaires?id_article='+id_article)