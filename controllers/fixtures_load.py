#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    ## TODO : Enlever le Quick fix sans obtenir l'erreur 'Cannot delete or update a parent row: a foreign key constraint fails'
    mycursor.execute('SET FOREIGN_KEY_CHECKS = 0;') ## Quick fix.
    sql='''DROP TABLE IF EXISTS ligne_panier, ligne_commande, gant, taille, type_gant, commande, etat, utilisateur, note_gant, commentaire_gant;'''
    mycursor.execute(sql)
    mycursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
    
    ## Table Utilisateur
    sql='''
    CREATE TABLE utilisateur (
                                 id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
                                 login VARCHAR(255) NOT NULL,
                                 email VARCHAR(255) NOT NULL,
                                 nom VARCHAR(255) NOT NULL,
                                 password VARCHAR(255) NOT NULL,
                                 role VARCHAR(255) NOT NULL,
                                 est_actif BOOLEAN NOT NULL
    ) DEFAULT CHARSET utf8;
    '''
    mycursor.execute(sql)
    
    ## Valeur Utilisateur
    sql=''' 
    INSERT INTO utilisateur(id_utilisateur,login,email,password,role,nom,est_actif) VALUES 
    (1,'admin','admin@admin.fr','pbkdf2:sha256:1000000$eQDrpqICHZ9eaRTn$446552ca50b5b3c248db2dde6deac950711c03c5d4863fe2bd9cef31d5f11988','ROLE_admin','admin','1'),
    (2,'client','client@client.fr','pbkdf2:sha256:1000000$jTcSUnFLWqDqGBJz$bf570532ed29dc8e3836245f37553be6bfea24d19dfb13145d33ab667c09b349','ROLE_client','client','1'),
    (3,'client2','client2@client2.fr','pbkdf2:sha256:1000000$qDAkJlUehmaARP1S$39044e949f63765b785007523adcde3d2ad9c2283d71e3ce5ffe58cbf8d86080','ROLE_client','client2','1');
    '''
    mycursor.execute(sql)

    ## Table Type_gant
    sql=''' 
    CREATE TABLE type_gant(
        id_type_gant INT AUTO_INCREMENT,
        nom_type_gant VARCHAR(255) NOT NULL,
        PRIMARY KEY (id_type_gant)
    )  DEFAULT CHARSET utf8;  
    '''
    mycursor.execute(sql)
    
    ## Valeur Type_gant
    sql=''' 
    INSERT INTO type_gant(id_type_gant, nom_type_gant) VALUES 
    (NULL,'Moto'),
    (NULL, 'Ski'),
    (NULL, 'Golf'),
    (NULL, 'Jardinage');
    '''
    mycursor.execute(sql)

    ## Table Etat
    sql=''' 
    CREATE TABLE etat (
        id_etat INT AUTO_INCREMENT,
        libelle_etat VARCHAR(255) NOT NULL,
        PRIMARY KEY(id_etat)
    )  DEFAULT CHARSET=utf8;  
    '''
    mycursor.execute(sql)
    
    ## Valeur Etat
    sql = ''' 
    INSERT INTO etat(id_etat, libelle_etat) VALUES 
    (1,'En cours de préparation'),
    (2,'Expédiée');
     '''
    mycursor.execute(sql)
    
    
    ## Table Taille
    sql = '''
        CREATE TABLE taille (
            id_taille INT PRIMARY KEY AUTO_INCREMENT,
            num_taille_fr INT NOT NULL,
            taille_us_homme VARCHAR(255) NOT NULL,
            taille_us_femme VARCHAR(255) NOT NULL,
            tour_de_main FLOAT NOT NULL
        ) DEFAULT CHARSET=utf8;
        '''
    mycursor.execute(sql)

    ## Valeur Taille
    sql = '''
    INSERT INTO taille(id_taille,num_taille_fr,taille_us_homme,taille_us_femme,tour_de_main) VALUES
                                                                                             (1,6.5,'NULL','S',17.5),
                                                                                             (2,7,'NULL','M',19),
                                                                                             (3,7.5,'NULL','L',20),
                                                                                             (4,8,'S','XL',21.5),
                                                                                             (5,8.5,'M','XXL',23),
                                                                                             (6,9,'L','NULL',24),
                                                                                             (7,9.5,'XL','NULL',25.5),
                                                                                             (8,10,'XXL','NULL',27);                                                                                                                                                                                       
    '''
    mycursor.execute(sql)

    ## Table Gant
    sql='''
    CREATE TABLE gant (
        id_gant INT PRIMARY KEY AUTO_INCREMENT,
        nom_gant VARCHAR(255) NOT NULL,
        poids FLOAT NOT NULL,
        couleur VARCHAR(255) NOT NULL,
        prix_gant FLOAT NOT NULL,
        taille_id INT NOT NULL,
        description TEXT,
        type_gant_id INT NOT NULL,
        fournisseur VARCHAR(255) NOT NULL,
        marque VARCHAR(255) NOT NULL,
        stock INT NOT NULL DEFAULT 0,
        nb_notes INT NOT NULL DEFAULT 0,
        moyenne_notes_gant DECIMAL(10, 2) DEFAULT 0.00,
        image VARCHAR(255) NOT NULL,
        CONSTRAINT fk_gant_taille FOREIGN KEY (taille_id) REFERENCES taille(id_taille),
        CONSTRAINT fk_gant_type_gant FOREIGN KEY (type_gant_id) REFERENCES type_gant(id_type_gant)

    )  DEFAULT CHARSET=utf8;  
     '''
    mycursor.execute(sql)
    
    ## Valeur Gant
    sql = ''' 
    INSERT INTO gant(nom_gant,poids,couleur,prix_gant,taille_id,type_gant_id,fournisseur,marque,stock,image) VALUES
                                                                                                               ('Gants moto dainese ','120','Noir/rouge','85','1','1','Dainese SpA','dainese','3','gant_moto1.jpg'),
                                                                                                               ('Gants moto DXR GAMEPAD','134','Noire','25.12','2','1','Bihr','DXR','5','gant_moto2.jpg'),
                                                                                                               ('Gants moto Alpinestars','146','Vert / Noir','35.10','3','1','Alpinestars','Alpinestars ','34','gant_moto3.jpg'),
                                                                                                               ('Gants Ixon RS RISE AIR','169','Noir / Rouge','56.96','4','1','Ixon','Ixon','22','gant_moto4.jpg'),
                                                                                                               ('Gants cuir/textile Bering Austral GTX','198','marine/gris/rouge','94','5','1','Bering','Bering ','7','gant_moto5.webp'),
                                                                                                               ('HERCULE','134','Beige/rouge','140','2','2','CimAlp','CimAlp','6','gant_ski1.jpg'),
                                                                                                               ('Gants de Ski Hiver Tactiles Imperméables ','175','Gris','85','3','2','Decathlon','Body Technology','3','gant_ski2.webp'),
                                                                                                               ('GANTS DE SKI HOMME REUSH SNOW SPIRIT GORE-TEX ','170','Noir','45','2','2','Reusch International','REUSH','51','gant_ski3.avif'),
                                                                                                               ('Gants de ski chauds adulte  ','120','blanc','25','7','2','Decathlon','Wedze','65','gant_ski4.avif'),
                                                                                                               ('Gants de ski chauffants EVO-2 Adulte ','120','Noir/rouge','149','1','2','G-Heat','G-Heat','43','gant_ski5.avif'),
                                                                                                               ('Gant golf droitier Footjoy Homme - Gtxreme','134','Blanc','21','2','3','Acushnet','FootJoy','22','gant_golf1.avif'),
                                                                                                               ('GANT GOLF STRATUS DROITIER HOMME ','189','Blanc','17','6','3','TaylorMade','Taylormade','97','gant_golf2.avif'),
                                                                                                               ('Paire de gants golf pluie homme - RW ','170','Noir','15','8','3','Decathlon','Inesis','103','gant_golf3.avif'),
                                                                                                               ('Gant Aditech 24','168','blanc','20','5','3','Adidas AG','Adidas','12','gant_golf4.avif'),
                                                                                                               ('Nike Tech Extreme 7','120','Blanc/Noir','24.99','1','3','Nike Inc','Nike','14','gant_golf5.webp'),
                                                                                                               ('Gant de travail jardinier - SOLIDUR CERCIS GA08','42','Beige / Noir','16.25','1','4','Solidur','Solidur','2','gant_jardinage1.jpg'),
                                                                                                               ('Paire de gants pour les travaux de jardinage latex, T 6 ','67','vert','4.19','3','4','Geolia','GEOLIA','3','gant_jardinage2.webp'),
                                                                                                               ('GANTS DE JARDIN SPECIAL EPINEUX','78','vert','7.76','6','4','Europapa','Europapa','105','gant_jardinage3.jpg'),
                                                                                                               ('WZQH Gants De Travail En Cuir Pour Hommes Ou Femmes','92',' Café/gris','11.99','7','4','WZQH','WZQH','5','gant_jardinage4.jpg'),
                                                                                                               ('Gants imprimés de jardinage','51','Noir/Marron','12.08','1','4','Garden Trading','sans-marque','71','gant_jardinage5.jpg');
    '''
    mycursor.execute(sql)

    ## Table Commande
    sql = '''
    CREATE TABLE commande (
        id_commande INT PRIMARY KEY AUTO_INCREMENT,
        date_achat DATE NOT NULL,
        utilisateur_id INT NOT NULL,
        etat_id INT NOT NULL,
        CONSTRAINT fk_commande_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        CONSTRAINT fk_commande_etat FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
    ) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    ## Valeur Commande
    sql = ''' 
    INSERT INTO commande(id_commande, date_achat, utilisateur_id, etat_id) VALUES
                                                                           (2, '2023-12-15', 3, 1),
                                                                           (3, '2024-01-10', 2, 2);
    '''
    mycursor.execute(sql)

    ## Table Ligne_commande
    sql = ''' 
    CREATE TABLE ligne_commande(
        commande_id INT NOT NULL,
        gant_id INT NOT NULL,
        prix FLOAT NOT NULL,
        quantite INT NOT NULL,
        CONSTRAINT fk_ligne_commande_commande FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
        CONSTRAINT fk_ligne_commande_gant FOREIGN KEY (gant_id) REFERENCES gant(id_gant)
    ) DEFAULT CHARSET=utf8;
    '''
    mycursor.execute(sql)

    ## Valeur Ligne_commande
    sql = '''
    INSERT INTO ligne_commande(commande_id, gant_id, prix, quantite) VALUES
                                                                     (2, 6, 140, 1),
                                                                     (2, 8, 56.96, 2),
                                                                     (3, 12, 15, 3),
                                                                     (3, 18, 11.99, 4);
    '''
    mycursor.execute(sql)

    ## Table Ligne_commande
    sql = '''
    CREATE TABLE ligne_panier(
        utilisateur_id INT NOT NULL,
        gant_id INT NOT NULL,
        quantite INT NOT NULL,
        date_ajout DATE NOT NULL,
        CONSTRAINT fk_ligne_panier_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        CONSTRAINT fk_ligne_panier_gant FOREIGN KEY (gant_id) REFERENCES gant(id_gant)
    );  
         '''
    mycursor.execute(sql)
    
    ## Table Ligne_commande
    sql = '''
    INSERT INTO ligne_panier(utilisateur_id, gant_id, quantite, date_ajout) VALUES
    (1,1,1,'2021-01-01'),
    (2,2,2,'2021-01-02'),
    (3,3,3,'2021-01-03');

    '''
    mycursor.execute(sql)

    ## Table Commentaire
    sql = '''
    CREATE TABLE commentaire_gant (
        commentaire_gant_id INT PRIMARY KEY AUTO_INCREMENT,
        commentaire TEXT,
        utilisateur_id INT NOT NULL,
        gant_id INT NOT NULL,
        date_redaction DATE NOT NULL,
        valider TINYINT(1) DEFAULT 0,
        CONSTRAINT fk_commentaire_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        CONSTRAINT fk_commentaire_gant FOREIGN KEY (gant_id) REFERENCES gant(id_gant)
    );
    '''
    mycursor.execute(sql)

    ## Valeur Commentaire
    sql = '''
    INSERT INTO commentaire_gant(commentaire, utilisateur_id, gant_id, date_redaction, valider) 
    SELECT 'Bienvenu dans la section commentaire' AS commentaire, 1 AS utilisateur_id, id_gant AS gant_id, NOW() AS date_redaction, 1 AS valider 
    FROM gant;
    '''
    mycursor.execute(sql)


    ## Table Note
    sql='''
    CREATE TABLE note_gant (
        note_gant_id INT PRIMARY KEY AUTO_INCREMENT,
        note INT NOT NULL,
        utilisateur_id INT NOT NULL,
        gant_id INT NOT NULL,
        CONSTRAINT fk_note_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
        CONSTRAINT fk_note_gant FOREIGN KEY (gant_id) REFERENCES gant(id_gant)
    );
    '''
    mycursor.execute(sql)

    ## Valeur Note

    sql = '''
    INSERT INTO note_gant(note, utilisateur_id, gant_id) 
    SELECT 1 AS note, 1 AS utilisateur_id, id_gant 
    FROM gant;
    '''
    
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')
