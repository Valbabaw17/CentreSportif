import sqlite3
import sqlite3 as sqlite
import sys
from datetime import datetime as dt
from flask import Flask, render_template, request, url_for, redirect,session,Response    #importe l'objet flask, le render_template(pour templates), redirect et url_for (pour redircetion), session pour sessions


conn = sqlite3.connect('database.sqlite')
cursorObj = conn.cursor()

app = Flask(__name__)
app.secret_key = 'cle secrete'  #cle secrete pour les session pour cryper la session pour rendre le systeme plus fiable

def get_db_connection():                            #fonction pour retourne l'accès à la base de données
    connection = sqlite3.connect('database.sqlite')
    connection.row_factory = sqlite3.Row
    return connection

#################################################
#              PARTIE POS                       #
#                                               #
#################################################
##  ROUTES   ###
#Route par défaut pour la page d'accueil#
@app.route('/')                         #decorateur qui transforme une fonction python en fonction d'affichage flask
@app.route('/index')
def index():  # retourne le texte suivant
    return render_template('index.html')

#Page POS#
@app.route('/POSpage',methods=('GET','POST'))
def POSpage():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        date_naissance = request.form['date_naissance']
        rue = request.form['rue']
        numero_rue = request.form['numero_rue']
        code_postal = request.form['code_postal']
        localite = request.form['localite']
        numero_telephone = request.form['numero_telephone']

        conn = get_db_connection()
        conn.execute('INSERT INTO membres VALUES (NULL,?, ?,?, ?, ?, ?, ?, ?,datetime(\'now\',\'localtime\'))',
                     # insertion dans la base de données
                     (nom, prenom,date_naissance, rue, numero_rue, code_postal, localite, numero_telephone));
        conn.commit()
        conn.close()

    return render_template('POSpage.html')

#Page Comptable#
@app.route('/comptablepage')
def comptablepage():
    return render_template('comptablepage.html')


#Accès à la DB en renvoyant les informations vers des fichiers xml#
#Liste des membres#
@app.route('/membres', methods=('GET','POST'))
def infos_membres():
        conn = get_db_connection()
        membres = conn.execute('SELECT * FROM membres').fetchall()
        conn.commit()
        conn.close()
        return Response(render_template("membres.xml",membres=membres), content_type="text/xml")

#Liste des abonnements avec les noms+prenoms+telephone#
@app.route('/abonnements', methods=('GET','POST'))
def abonnements():
        conn = get_db_connection()
        informations = conn.execute('SELECT * FROM membres LEFT JOIN abonnements a on membres.id_membre = a.id_membre').fetchall()
        conn.commit()
        conn.close()
        return Response(render_template("abonnements.xml", informations=informations), content_type='text/xml')

#Ajouter un abonnement
@app.route('/ajouter_abonnements', methods=('GET','POST'))
def ajouter_abonnements():
    if request.method == 'POST':
        id_membre = request.form['id_membre']
        seances_totales = request.form['seances_totales']

        #Insérer l'abonnement dans la table abonnement
        conn1 = get_db_connection()
        conn1.execute('INSERT INTO abonnements VALUES (NULL,?, ?, datetime(\'now\',\'localtime\'), ?, ?)',  #insertion dans la base de données
                         (seances_totales, seances_totales, id_membre,1))
        conn1.commit()

        #Sélectionner l'id formule qui correspond à l'abonnement ajouté
        conn2 = get_db_connection()
        id_formule  = conn2.execute(
            'SELECT journal.id_formule FROM journal INNER JOIN formules_abonnements on journal.id_formule = formules_abonnements.id_formule WHERE formules_abonnements.nombre_seances = ?',
            (seances_totales))
        conn2.commit()
        conn2.close()

        #Récupérer l'id formule et l'ajouter à la table journal avec l'id client
        conn3 = get_db_connection()
        conn3.execute('INSERT INTO journal VALUES (NULL,?, ?, NULL, NULL)',
                      # insertion dans la base de données
                      (id_membre, id_formule))
        conn3.commit()
        conn3.close()

    return redirect(url_for('POSpage'))

#Decrementer du nombre de séance choisie
@app.route('/ajouter_seances', methods=('GET','Post'))
def ajouter_seances():
    if request.method == 'POST':
        id_membre_requete = request.form['id_membre']
        seances_choisies_requete = request.form['seances_choisies']

        conn = get_db_connection()
        conn.execute("""UPDATE abonnements SET seances_dispo=seances_dispo-? WHERE id_membre = ?""",(seances_choisies_requete,id_membre_requete))
        conn.commit()
        conn.close()
        return redirect(url_for("POSpage"))

#Liste des marchandises
@app.route('/marchandises', methods=('GET','POST'))
def marchandises():
    conn = get_db_connection()
    marchandises = conn.execute('SELECT * FROM marchandises').fetchall()
    conn.commit()
    conn.close()
    return Response(render_template("marchandises.xml", marchandises=marchandises), content_type='text/xml')

@app.route('/ajouter_marchandises', methods=('GET','POST'))
def ajouter_marchandises():
    if request.method == 'POST':
        num_membre = request.form['id_membre']
        id_membre = int(num_membre)
        marchandises = request.form['marchandises']
        quantites = request.form['quantites']

        conn = get_db_connection()
        id_marchandise = conn.execute('SELECT id_marchandise FROM marchandises WHERE nom =? ',(marchandises,)).fetchone()[0]
        total_transaction = conn.execute('SELECT prix FROM marchandises WHERE nom =? ',(marchandises,)).fetchone()[0]

        conn.execute('INSERT INTO journal VALUES (NULL,?,NULL,?,?,?,date(\'now\'),time("now", "localtime"))',
                     (id_membre, id_marchandise, quantites, total_transaction))
        conn.commit()
        conn.close()
    return redirect(url_for('POSpage'))



#################################################
#              PARTIE COMPTABLE                 #
#                                               #
#################################################
@app.route('/formulaire_jour' , methods=('GET', 'POST'))        #retourne un new membre suite au form de la page inscription
def formulaire_jour():
    if request.method == 'POST':
        jour_transaction = request.form['jour_transaction']
        session["jour_transaction"] = jour_transaction

        return redirect(url_for('liste_detaillee'))
    return render_template('formulaire_jour.html')

@app.route('/liste_detaillee')
def liste_detaillee():
        jour = session["jour_transaction"]
        conn = get_db_connection()
        liste_detaillee = conn.execute('SELECT * FROM journal INNER JOIN marchandises m on journal.id_marchandise = m.id_marchandise').fetchall()
        conn.commit()
        conn.close()
        return render_template("liste_detaillee.html",liste_detaillee=liste_detaillee, jour=jour)

@app.route('/formulaire_mois' , methods=('GET', 'POST'))        #retourne un new membre suite au form de la page inscription
def formulaire_mois():
    if request.method == 'POST':
        mois_transaction = request.form['mois_transaction']
        session["mois_transaction"] = mois_transaction

        return redirect(url_for('total_jour_jour'))
    return render_template('formulaire_mois.html')

@app.route('/total_jour_jour')
def total_jour_jour():
    conn = get_db_connection()
    mois_selectione = int(session["mois_transaction"])

    if mois_selectione < 10:
        mois_transaction = "0"+session["mois_transaction"]
    else:
        mois_transaction = session["mois_transaction"]

    total_jour_jour = conn.execute(
        'SELECT jour_transaction,SUM(total_transaction),strftime(\'%m\',jour_transaction) FROM journal GROUP BY jour_transaction').fetchall()

    total_final_mois = conn.execute('SELECT SUM(total_transaction) FROM journal WHERE strftime(\'%m\',jour_transaction) == ?  GROUP BY strftime(\'%m\',jour_transaction)',(mois_transaction,)).fetchone();
    conn.commit()
    conn.close()
    return render_template('total_jour_jour.html',total_jour_jour=total_jour_jour,mois_transaction=mois_transaction,total_final_mois=total_final_mois)

@app.route('/formulaire_annee' , methods=('GET', 'POST'))
def formulaire_annee():
    if request.method == 'POST':
        annee_transaction = request.form['annee_transaction']
        session["annee_transaction"] = annee_transaction

        return redirect(url_for('total_mois_mois'))
    return render_template('formulaire_annee.html')

@app.route('/total_mois_mois')
def total_mois_mois():
    conn = get_db_connection()
    annee_transaction = session["annee_transaction"]
    total_mois_mois = conn.execute(
        'SELECT strftime(\'%m\',jour_transaction),SUM(total_transaction),strftime(\'%Y\',jour_transaction) FROM journal GROUP BY strftime(\'%m\',jour_transaction);').fetchall()

    total_final_annee = conn.execute(
        'SELECT SUM(total_transaction) FROM journal WHERE strftime(\'%Y\',jour_transaction) == ? GROUP BY strftime(\'%Y\',jour_transaction)',(annee_transaction,)).fetchone();
    conn.commit()
    conn.close()
    return render_template('total_mois_mois.html',annee_transaction=annee_transaction,total_mois_mois=total_mois_mois,total_final_annee=total_final_annee)

@app.route('/liste_abonnements')
def liste_abonnements():
    return render_template('liste_abonnements.html')


@app.route('/nombre_moyen_exemplaires')
def nombre_moyen_exemplaires():
    return render_template('nombre_moyen_exemplaires.html')


@app.route('/nombre_moyen_personnes')
def nombre_moyen_personnes():
    return render_template('nombre_moyen_personnes.html')


@app.route('/personnes_presentes')
def personnes_presentes():
    return render_template('personnes_presentes.html')