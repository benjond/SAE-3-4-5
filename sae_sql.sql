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
                      fournisseur VARCHAR(255) NOT NULL,
                      marque VARCHAR(255) NOT NULL,
                      stock INT NOT NULL DEFAULT 0,
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


INSERT INTO etat(id_etat,libelle) VALUES
                                      (1,'En attente'),
                                      (2,'En cours de préparation'),
                                      (3,'Expédiée'),
                                      (4,'Livrée');

INSERT INTO type_gant(id_type_gant,nom_type_gant) VALUES
                                                      (NULL,'moto'),
                                                      (NULL, 'Ski'),
                                                      (NULL, 'golf'),
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





INSERT INTO commande(id_commande, date_achat, utilisateur_id, etat_id) VALUES
                                                                           (1, '2023-12-10', 2, 1),
                                                                           (2, '2023-12-15', 3, 2),
                                                                           (3, '2024-01-10', 2, 3);

INSERT INTO ligne_commande(commande_id, gant_id, prix, quantite) VALUES
                                                                     (2, 6, 140, 1), -- Commande d'un gant de ski "HERCULE" pour 140 €
                                                                     (2, 8, 56.96, 2), -- Commande de 2 paires de gants moto Ixon
                                                                     (3, 12, 15, 3), -- Commande de 3 paires de gants de golf "RW"
                                                                     (3, 18, 11.99, 4); -- Commande de 4 paires de gants de jardin "WZQH"

INSERT INTO ligne_panier(utilisateur_id, gant_id, quantite, date_ajout) VALUES
                                                                            (3, 7, 1, '2024-01-11'), -- L'utilisateur 3 ajoute un gant de ski chauffant
                                                                            (3, 16, 2, '2024-01-11'), -- L'utilisateur 3 ajoute 2 paires de gants de jardin "Europapa"
                                                                            (2, 4, 1, '2024-01-10'), -- L'utilisateur 2 ajoute un gant moto "Ixon"
                                                                            (2, 14, 1, '2024-01-10'); -- L'utilisateur 2 ajoute un gant de golf "Nike"


SELECT commande.id_commande, commande.date_achat, utilisateur.nom AS nom_utilisateur, etat.libelle AS etat_commande
FROM commande
INNER JOIN utilisateur ON commande.utilisateur_id = utilisateur.id_utilisateur
INNER JOIN etat ON commande.etat_id = etat.id_etat;

SELECT utilisateur.id_utilisateur, utilisateur.nom, commande.id_commande, commande.date_achat
FROM utilisateur
LEFT JOIN commande ON utilisateur.id_utilisateur = commande.utilisateur_id;


SELECT gant.id_gant, gant.nom_gant, ligne_commande.commande_id, ligne_commande.quantite
FROM gant
RIGHT JOIN ligne_commande ON gant.id_gant = ligne_commande.gant_id;

SELECT commande.id_commande, commande.date_achat, ligne_commande.gant_id, ligne_commande.quantite
FROM commande
LEFT JOIN ligne_commande ON commande.id_commande = ligne_commande.commande_id;SELECT utilisateur.id_utilisateur, utilisateur.nom, ligne_panier.gant_id, ligne_panier.quantite
FROM utilisateur
LEFT JOIN ligne_panier ON utilisateur.id_utilisateur = ligne_panier.utilisateur_id;




