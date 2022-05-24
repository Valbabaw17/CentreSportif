import sqlite3
import sqlite3 as sqlite
from flask import Flask, render_template, request, url_for, redirect,session,Response    #importe l'objet flask, le render_template(pour templates), redirect et url_for (pour redircetion), session pour sessions

app = Flask(__name__)
app.secret_key = 'cle secrete'  #cle secrete pour les session pour cryper la session pour rendre le systeme plus fiable

def get_db_connection():                            #fonction pour retourne l'accès à la base de données
    connection = sqlite3.connect('database.sqlite')
    connection.row_factory = sqlite3.Row
    return connection

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
        rue = request.form['rue']
        numero_rue = request.form['numero_rue']
        code_postal = request.form['code_postal']
        localite = request.form['localite']
        numero_telephone = request.form['numero_telephone']
        seances_choisies = request.form['seances_choisies']

        conn = get_db_connection()
        conn.execute('INSERT INTO membres VALUES (NULL,?, ?, ?, ?, ?, ?, ?,datetime(\'now\',\'localtime\'))',
                     # insertion dans la base de données
                     (nom, prenom, rue, numero_rue, code_postal, localite, numero_telephone))
        conn.execute('INSERT INTO abonnements VALUES (NULL,?, ?, datetime(\'now\',\'localtime\'), con.sqlite_master.ROWID, ?)',
                     # insertion dans la base de données
                     (seances_choisies, seances_choisies, 1))
        conn.commit()
        conn.close()
    return render_template('POSpage.html')

#Page Comptable#
@app.route('/comptablepage')
def comptablepage():
    return render_template('comptablepage.html')


#Accès à la DB en renvoyant les informations vers des fichiers xml#
@app.route('/infos_membres', methods=('GET','POST'))
def infos_membres():
        conn = get_db_connection()
        membres = conn.execute('SELECT * FROM membres').fetchall()
        conn.commit()
        conn.close()
        return Response(render_template("infos_membres.xml",membres=membres), content_type="text/xml")

@app.route('/abonnements', methods=('GET','POST'))
def abonnements():
        conn = get_db_connection()
        informations = conn.execute('SELECT * FROM membres LEFT JOIN abonnements a on membres.id_membre = a.id_membre').fetchall()
        conn.commit()
        conn.close()
        return Response(render_template("abonnements.xml", informations=informations), content_type='text/xml')
