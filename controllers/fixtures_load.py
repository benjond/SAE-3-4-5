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
    sql='''DROP TABLE IF EXISTS ligne_panier, ligne_commande, gant, taille, type_gant, commande, etat, utilisateur;'''

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
    (1,'admin','admin@admin.fr','pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988','1','admin','1'),
    (2,'client','client@client.fr','pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349','0','client','1'),
    (3,'client2','client2@client2.fr','pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080','0','client2','1');
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
    INSERT INTO type_gant(id_type_gant, libelle) VALUES 
    (NULL,'Boxe'),
    (NULL, 'Ski'),
    (NULL, 'Golf'),
    (NULL, 'Jaradinage');
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
    INSERT INTO etat(etat_id, libelle) VALUES 
    (1,'En attente'),
    (2,'En cours de préparation'),
    (3,'Expédiée'),
    (4,'Livrée');
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
    INSERT INTO taille(id_taille, num_taille_fr, taille_us, tour_de_main) VALUES
    (1,6.5,'S',17.5),
    (2,7,'M',19),
    (3,7.5,'L',20),
    (4,8,'XL',21.5),
    (5,8.5,'XXL',23),
    (6,9,'NULL',24),
    (7,9.5,'NULL',25.5),
    (8,10,'NULL',27);
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
        image VARCHAR(255) NOT NULL,
        CONSTRAINT fk_gant_taille FOREIGN KEY (taille_id) REFERENCES taille(id_taille),
        CONSTRAINT fk_gant_type_gant FOREIGN KEY (type_gant_id) REFERENCES type_gant(id_type_gant)

    )  DEFAULT CHARSET=utf8;  
     '''
    mycursor.execute(sql)
    sql = ''' 
    INSERT INTO gant(id_gant, nom_gant, poids, couleur, prix_gant, taille_id, type_gant_id, fournisseur, marque, image) VALUES
    (1,'Gant de boxe',0.5,'rouge',50,1,1,1,'Everlast','gant_boxe.jpg'),
    (2,'Gant de ski',0.6,'bleu',60,2,2,2,'Rossignol','gant_ski.jpg'),
    (3,'Gant de golf',0.7,'vert',70,3,3,3,'Titleist','gant_golf.jpg'),
    (4,'Gant de jaradinage',0.8,'jaune',80,4,4,4,'Gardena','gant_jardinage.jpg');
         '''
    mycursor.execute(sql)




    sql = '''
  CREATE TABLE commande (
      id_commande INT PRIMARY KEY AUTO_INCREMENT,
      date_achat DATE NOT NULL,
      utilisateur_id INT NOT NULL,
      etat_id INT NOT NULL,
      CONSTRAINT fk_commande_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
      CONSTRAINT fk_commande_etat FOREIGN KEY (etat_id) REFERENCES etat(etat_id)
  ) DEFAULT CHARSET=utf8;
  '''
    mycursor.execute(sql)

    sql = ''' 
   INSERT INTO commande(id_commande, date_achat, utilisateur_id, etat_id) VALUES
   (1,'2021-01-01',1,1),
   (2,'2021-01-02',2,2),
   (3,'2021-01-03',3,3);
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
    INSERT INTO ligne_commande(commande_id, gant_id, prix, quantite) VALUES
   (1,1,50,1),
   (2,2,60,2),
   (3,3,70,3);
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
    sql = '''
    INSERT INTO ligne_panier(utilisateur_id, gant_id, quantite, date_ajout) VALUES
    (1,1,1,'2021-01-01'),
    (2,2,2,'2021-01-02'),
    (3,3,3,'2021-01-03');

    '''
    mycursor.execute(sql)


    get_db().commit()
    return redirect('/')
