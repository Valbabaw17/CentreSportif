/*Création des tables*/
CREATE TABLE membres(
    id_membre INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    nom_rue TEXT NOT NULL,
    numero_rue INTEGER NOT NULL,
    code_postal INTEGER NOT NULL,
    localite TEXT NOT NULL,
    num_telephone INTEGER NOT NULL,
    date_inscription TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE abonnements(
    id_abonnement INTEGER PRIMARY KEY AUTOINCREMENT,
    seances_dispo INTEGER,
    seances_totale INTEGER NOT NULL,
    date_achat TEXT NOT NULL,
    id_membre  INTEGER NOT NULL,
    FOREIGN KEY (id_membre) REFERENCES membres (id_membre)
);
ALTER TABLE abonnements ADD etat_abonnement NUMERIC;
CREATE TABLE marchandises(
    id_marchandise INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prix REAL NOT NULL,
    quantite INTEGER NOT NULL
);

CREATE TABLE formules_abonnements(
    id_formule INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_seances INTEGER NOT NULL,
    prix_formule REAL NOT NULL
);

CREATE TABLE journal(
    id_journal INTEGER PRIMARY KEY AUTOINCREMENT,
    id_formule INTEGER NOT NULL,
    id_marchandise INTEGER NOT NULL,
    quantite_marchandise INTEGER NOT NULL,
    id_abonnement INTEGER NOT NULL,
    FOREIGN KEY (id_formule) REFERENCES formules_abonnements(id_formule),
    FOREIGN KEY (id_marchandise) REFERENCES marchandises(id_marchandise),
    FOREIGN KEY (id_abonnement) REFERENCES abonnements(id_abonnement)
);

CREATE TABLE depart_arrivees(
    id_depart_arrivee INTEGER PRIMARY KEY AUTOINCREMENT,
    heure_arrivee TEXT NOT NULL,
    duree_seance INTEGER NOT NULL,
    id_abonnement INTEGER NOT NULL,
    FOREIGN KEY (id_abonnement) REFERENCES abonnements(id_abonnement)
);