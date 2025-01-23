#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql='''DROP TABLE IF EXISTS ligne_panier, ligne_commande, gant, taille, type_gant, commmande, etat, utilisateur;'''

    mycursor.execute(sql)
    sql='''
    CREATE TABLE utilisateur(
        id_utilisateur INT AUTO_INCREMENT,
        login VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255),
        role boolean,
        nom VARCHAR(255),
        est_actif boolean,
        PRIMARY KEY (id_utilisateur)
    )  DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)
    sql=''' 
    INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES
(1,'admin','admin@admin.fr',
    'pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988',
    'ROLE_admin','admin','1'),
(2,'client','client@client.fr',
    'pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349',
    'ROLE_client','client','1'),
(3,'client2','client2@client2.fr',
    'pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080',
    'ROLE_client','client2','1');
    '''
    mycursor.execute(sql)


    sql=''' 
    CREATE TABLE type_gant(
        id_type_gant INT AUTO_INCREMENT,
        libelle VARCHAR(255) NOT NULL,
        PRIMARY KEY (id_type_gant)
    )  DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)
    sql=''' 
INSERT INTO type_gant()
    '''
    mycursor.execute(sql)


    sql=''' 
    CREATE TABLE etat (
        etat_id INT AUTO_INCREMENT,
        libelle VARCHAR(255) NOT NULL,
        PRIMARY KEY(etat_id)
    )  DEFAULT CHARSET=utf8;  
    '''
    mycursor.execute(sql)
    sql = ''' 
INSERT INTO etat ()
     '''
    mycursor.execute(sql)


    sql = ''' 
    CREATE TABLE gant (
        id_gant INT PRIMARY KEY AUTO_INCREMENT,
        nom_gant VARCHAR(255) NOT NULL,
        poids FLOAT NOT NULL,
        couleur VARCHAR(255) NOT NULL,
        prix_gant FLOAT NOT NULL,
        taille_id INT NOT NULL,
        type_gant_id INT NOT NULL,
        fournisseur INT NOT NULL,
        marque VARCHAR(255) NOT NULL,
        CONSTRAINT fk_gant_taille FOREIGN KEY (taille_id) REFERENCES taille(id_taille),
        CONSTRAINT fk_gant_type_gant FOREIGN KEY (type_gant_id) REFERENCES type_gant(id_type_gant)

    )  DEFAULT CHARSET=utf8;  
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO article ()
         '''
    mycursor.execute(sql)


    sql = '''
    CREATE TABLE taille (
        id_taille INT PRIMARY KEY AUTO_INCREMENT,
        num_taille_fr INT NOT NULL,
        taille_us VARCHAR(255) NOT NULL,
        tour_de_main FLOAT NOT NULL
    ) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)
    sql = '''
    INSERT INTO taille ()
    '''
    mycursor.execute(sql)


    sql = ''' 
    CREATE TABLE commande (
        id_commande INT AUTO_INCREMENT,
        date_achat DATE,
        id_utilisateur INT,
        etat_id INT,
        FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
        FOREIGN KEY (etat_id) REFERENCES etat(etat_id),
        PRIMARY KEY(id_commande)
    ) DEFAULT CHARSET=utf8;  
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO commande 
                 '''
    mycursor.execute(sql)


    sql = ''' 
    CREATE TABLE ligne_commande(
        commande_id INT NOT NULL,
        gant_id INT NOT NULL,
        prix FLOAT NOT NULL,
        quantite INT NOT NULL,
        CONSTRAINT fk_ligne_commande_commande FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
        CONSTRAINT fk_ligne_commande_gant FOREIGN KEY (gant_id) REFERENCES gant(id_gant)
    );
         '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO ligne_commande ()
         '''
    mycursor.execute(sql)


    sql = ''' 
    CREATE TABLE ligne_panier (
        utilisateur_id INT NOT NULL,
        gant_id INT NOT NULL,
        quantite INT NOT NULL,
        date_ajout DATE NOT NULL,
        CONSTRAINT fk_ligne_panier_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        CONSTRAINT fk_ligne_panier_gant FOREIGN KEY (gant_id) REFERENCES gant(id_gant)
    );  
         '''
    mycursor.execute(sql)


    get_db().commit()
    return redirect('/')
