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
                      libelle VARCHAR(255) NOT NULL
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
                        taille_us VARCHAR(255) NOT NULL,
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
                                                    (NULL,'Boxe'),
                                                    (NULL, 'Ski'),
                                                    (NULL, 'Golf'),
                                                    (NULL, 'Jaradinage');

