from flask import Blueprint, request, render_template, session, redirect
from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__, template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')

@admin_commande.route('/admin/commande/show', methods=['get', 'post'])
def admin_commande_show():
    mycursor = get_db().cursor()

    # Récupérer toutes les commandes
    sql = '''SELECT commande.id_commande, commande.date_achat, utilisateur.login, etat.libelle_etat, 
                    COUNT(ligne_commande.gant_id) AS nbr_articles, 
                    ROUND(SUM(ligne_commande.quantite * ligne_commande.prix), 2) as prix_total, 
                    commande.etat_id
             FROM commande 
             JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
             JOIN etat ON commande.etat_id = etat.id_etat
             LEFT JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id
             GROUP BY commande.id_commande'''

    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    # Initialisation des variables pour une commande spécifique
    articles_commande = None

    id_commande = request.args.get('id_commande', None)
    if id_commande:
        sql_details = '''SELECT gant.nom_gant AS nom, 
                                ligne_commande.quantite, 
                                ligne_commande.prix,
                                ROUND((ligne_commande.quantite * ligne_commande.prix), 2) AS prix_ligne
                         FROM ligne_commande 
                         JOIN gant ON ligne_commande.gant_id = gant.id_gant
                         WHERE ligne_commande.commande_id = %s'''

        mycursor.execute(sql_details, (id_commande,))
        articles_commande = mycursor.fetchall()

    return render_template('admin/commandes/show.html',
                           commandes=commandes,
                           articles_commande=articles_commande)


@admin_commande.route('/admin/commande/valider', methods=['POST'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)

    if commande_id:
        sql = '''UPDATE commande
                 SET etat_id = 2
                 WHERE id_commande = %s'''
        mycursor.execute(sql, (commande_id,))
        get_db().commit()

    return redirect('/admin/commande/show')

