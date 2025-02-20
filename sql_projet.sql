DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS gant;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS type_gant;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;

CREATE TABLE utilisateur (
                             id_utilisateur INT PRIMARY KEY AUTO_INCREMENT,
                             login VARCHAR(255) NOT NULL,
                             email VARCHAR(255) NOT NULL,
                             nom VARCHAR(255) NOT NULL,
                             password VARCHAR(255) NOT NULL,
                             role VARCHAR(255) NOT NULL,
                             est_actif BOOLEAN NOT NULL
);

CREATE TABLE etat (
                      id_etat INT PRIMARY KEY AUTO_INCREMENT,
                      libelle_etat VARCHAR(255) NOT NULL
);

CREATE TABLE commande (
                          id_commande INT PRIMARY KEY AUTO_INCREMENT,
                          date_achat DATE NOT NULL,
                          utilisateur_id INT NOT NULL,
                          etat_id INT NOT NULL,
                          CONSTRAINT fk_commande_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                          CONSTRAINT fk_commande_etat FOREIGN KEY (etat_id) REFERENCES etat(id_etat)

);

CREATE TABLE type_gant (
                           id_type_gant  INT PRIMARY KEY AUTO_INCREMENT,
                           nom_type_gant VARCHAR(255) NOT NULL

);

CREATE TABLE taille (
                        id_taille INT PRIMARY KEY AUTO_INCREMENT,
                        num_taille_fr INT NOT NULL,
                        taille_us_homme VARCHAR(255) NOT NULL,
                        taille_us_femme VARCHAR(255) NOT NULL,
                        tour_de_main FLOAT NOT NULL
);


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

);



CREATE TABLE ligne_commande (
                                commande_id INT NOT NULL,
                                gant_id INT NOT NULL,
                                prix FLOAT NOT NULL,
                                quantite INT NOT NULL,
                                CONSTRAINT fk_ligne_commande_commande FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
                                CONSTRAINT fk_ligne_commande_gant FOREIGN KEY (gant_id) REFERENCES gant(id_gant)
);

CREATE TABLE ligne_panier (
                              utilisateur_id INT NOT NULL,
                              gant_id INT NOT NULL,
                              quantite INT NOT NULL,
                              date_ajout DATE NOT NULL,
                              CONSTRAINT fk_ligne_panier_utilisateur FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id_utilisateur),
                              CONSTRAINT fk_ligne_panier_gant FOREIGN KEY (gant_id) REFERENCES gant(id_gant)
);

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


INSERT INTO etat(id_etat,libelle_etat) VALUES
                                      (1,'En cours de préparation'),
                                      (2,'Expédiée');

INSERT INTO type_gant(id_type_gant,nom_type_gant) VALUES
                                                      (NULL,'Boxe'),
                                                      (NULL, 'Ski'),
                                                      (NULL, 'Golf'),
                                                      (NULL, 'Jaradinage');

INSERT INTO taille(id_taille,num_taille_fr,taille_us_homme,taille_us_femme,tour_de_main) VALUES
                                                                                             (1,6.5,'NULL','S',17.5),
                                                                                             (2,7,'NULL','M',19),
                                                                                             (3,7.5,'NULL','L',20),
                                                                                             (4,8,'S','XL',21.5),
                                                                                             (5,8.5,'M','XXL',23),
                                                                                             (6,9,'L','NULL',24),
                                                                                             (7,9.5,'XL','NULL',25.5),
                                                                                             (8,10,'XXL','NULL',27);

INSERT INTO gant(id_gant,nom_gant,poids,couleur,prix_gant,taille_id,type_gant_id,fournisseur,marque,image) VALUES
                                                                                                               (NULL,'Gant de boxe en cuir','0.5','Noir','50','1','1','1','Everlast','gant1.jpg'),
                                                                                                               (NULL,'Gant de boxe en cuir','0.5','Rouge','50','2','1','1','Everlast','gant2.jpg'),
                                                                                                               (NULL,'Gant de boxe en cuir','0.5','Bleu','50','3','1','1','Everlast','gant3.jpg'),
                                                                                                               (NULL,'Gant de boxe en cuir','0.5','Blanc','50','4','1','1','Everlast','gant4.jpg'),
                                                                                                               (NULL,'Gant de boxe en cuir','0.5','Noir','50','5','1','1','Everlast','gant5.jpg');

INSERT INTO commande(id_commande,date_achat,utilisateur_id,etat_id) VALUES
                                                                      (1,'2020-01-01','2','1');

INSERT INTO ligne_commande(commande_id,gant_id,prix,quantite) VALUES
                                                                  (1,1,'50','1'),
                                                                  (1,2,'50','1'),
                                                                  (1,3,'50','1'),
                                                                  (1,4,'50','1'),
                                                                  (1,5,'50','1');

INSERT INTO ligne_panier(utilisateur_id,gant_id,quantite,date_ajout) VALUES
                                                                         (2,1,'1','2020-01-01'),
                                                                         (2,2,'1','2020-01-01'),
                                                                         (2,3,'1','2020-01-01'),
                                                                         (2,4,'1','2020-01-01'),
                                                                         (2,5,'1','2020-01-01');



