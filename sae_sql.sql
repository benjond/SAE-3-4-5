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
    role VARCHAR(255) NOT NULL
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


