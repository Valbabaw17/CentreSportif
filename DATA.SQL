/*INSERTION DE DONNEES*/
/*Ajout dans la table membres*/
INSERT INTO membres VALUES (NULL,'Jossart','Nico','Rue de la plage',2,6000,'Charleroi',0472437281,datetime('now','localtime')); /*datetime permet d'avoir la date au format ISO + heure actuelle*/
INSERT INTO membres VALUES (NULL,'Walbert','Valerio','Rue de la toure',3,6040,'Jumet',0493007221,datetime('now','localtime'));

/*Ajout dans la table abonnement*/
INSERT INTO abonnements VALUES(10,10,10,datetime('now','localtime'),1,TRUE); /*On commence à 10 en id_abonnement*/
INSERT INTO abonnements VALUES(11,20,20,datetime('now','localtime'),2,TRUE); /*On continue à 11 pour id_abonnement*/

/*Ajout dans la table formules abonnements*/
INSERT INTO formules_abonnements VALUES (1,10,19.99);    /*10 représente 10 heures de séances*/
INSERT INTO formules_abonnements VALUES (2,20,25.99);
INSERT INTO formules_abonnements VALUES (3,30,29.99);

/*Ajout dans la table marchandises*/
/*On commence le id_marchandise à 1*/
INSERT INTO marchandises VALUES (1,'Eau',2.00,100); /*On commence la quantité à 100 (stock) et on va décrémenter à chaque commande de membre*/
INSERT INTO marchandises VALUES (2,'Boisson énergisante',2.00,200);
INSERT INTO marchandises VALUES (3,'Coca',2.00,150);
INSERT INTO marchandises VALUES (4,'Jus',2.00,50);

/*Ajout dans la table journal*/
INSERT INTO journal VALUES (50,1,1,10);    /*On commence à 50 pour différencier les ID (on aurait pu commencé à 1*/
INSERT INTO journal VALUES (51,2,2,11);    /*On commence à 50 pour différencier les ID (on aurait pu commencé à 1*/

/*Ajout dans la table departs_arrivées*/
INSERT INTO depart_arrivees VALUES (1,'10h00',2,10);  /*2 représente 2 heures de séances*/
INSERT INTO depart_arrivees VALUES (2,'09h00',1,10);