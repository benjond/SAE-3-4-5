#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_article = Blueprint('admin_type_article', __name__,
                        template_folder='templates')

@admin_type_article.route('/admin/type-article/show')
def show_type_article():
    mycursor = get_db().cursor()
    sql = '''SELECT id_type_gant AS id_type_article, 
                    nom_type_gant AS libelle, 
                    (SELECT COUNT(*) FROM gant WHERE gant.type_gant_id = type_gant.id_type_gant) AS nbr_articles 
             FROM type_gant;'''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    print(types_article)  # Debug pour voir si les données sont bien récupérées
    return render_template('admin/type_article/show_type_article.html', types_article=types_article)


@admin_type_article.route('/admin/type-article/add', methods=['GET'])
def add_type_article():
    return render_template('admin/type_article/add_type_article.html')


@admin_type_article.route('/admin/type-article/add', methods=['POST'])
def valid_add_type_article():
    nom_type_gant = request.form.get('libelle', '')  # Récupération du champ du formulaire
    tuple_insert = (nom_type_gant,)

    mycursor = get_db().cursor()
    sql = ''' INSERT INTO type_gant (nom_type_gant) VALUES (%s); '''  # Correction du nom de la colonne
    mycursor.execute(sql, tuple_insert)

    get_db().commit()
    message = f'Type ajouté, libellé : {nom_type_gant}'
    flash(message, 'alert-success')

    return redirect('/admin/type-article/show')  # Redirection après l'ajout


@admin_type_article.route('/admin/type-article/delete', methods=['GET'])
def delete_type_article():
    id_type_article = request.args.get('id_type_article', '')
    mycursor = get_db().cursor()
    sql = '''DELETE FROM type_gant WHERE id_type_gant = %s;'''
    mycursor.execute(sql, (id_type_article,))
    get_db().commit()
    flash(u'suppression type article , id : ' + id_type_article, 'alert-success')
    return redirect('/admin/type-article/show')

@admin_type_article.route('/admin/type-article/edit', methods=['GET'])
def edit_type_article():
    id_type_article = request.args.get('id_type_article', '')
    mycursor = get_db().cursor()
    sql = '''SELECT id_type_gant, nom_type_gant FROM type_gant WHERE id_type_gant = %s'''
    mycursor.execute(sql, (id_type_article,))
    type_article = mycursor.fetchone()
    return render_template('admin/type_article/edit_type_article.html', type_article=type_article)

@admin_type_article.route('/admin/type-article/edit', methods=['POST'])
def valid_edit_type_article():
    libelle = request.form['libelle']
    id_type_article = request.form.get('id_type_article', '')
    tuple_update = (libelle, id_type_article)
    mycursor = get_db().cursor()
    sql = '''UPDATE type_gant SET nom_type_gant = %s WHERE id_type_gant = %s'''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(u'type article modifié, id: ' + id_type_article + " libelle : " + libelle, 'alert-success')
    return redirect('/admin/type-article/show')








