-- Ajouts Commentaire --
INSERT INTO commentaire_gant(commentaire, utilisateur_id, gant_id, date_redaction, valider)
VALUES "Les gants aditech sont d'une superbe qualité ! Je recommande !",2,14,NOW(),0;

INSERT INTO note_gant(note,utilisateur_id,gant_id)
VALUES 5,2,14;

INSERT INTO commentaire_gant(commentaire, utilisateur_id, gant_id, date_redaction, valider)
VALUES "Les gants Ixon RS RISE AIR sont confortable mais très fragile, après un tour de moto le cuir c'est déjà craquelé",3,4,NOW(),1;

INSERT INTO note_gant(note,utilisateur_id,gant_id)
VALUES 2,3,4;

INSERT INTO commentaire_gant(commentaire, utilisateur_id, gant_id, date_redaction, valider)
SELECT 'Attention une maintenance et prévue très prochainement' AS commentaire, 1 AS utilisateur_id, id_gant AS gant_id, NOW() AS date_redaction, 1 AS valider
