from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from celery import Celery
from scraper2 import scrape_company_details  # Import the scraping function

# Celery configuration
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  # Remplace par ton URI si nécessaire
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

# Initialize extensions
db = SQLAlchemy()
db.init_app(app)  # 🔹 Initialisation correcte avec `init_app`
celery = make_celery(app)

# Create tables in application context
with app.app_context():
    db.create_all()


# Fournisseur model (unchanged)
class Fournisseur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(120))
    site_web = db.Column(db.String(200))
    source = db.Column(db.String(100))
    micro_famille = db.Column(db.String(100))
    nature_produit = db.Column(db.String(100))
    type_activite = db.Column(db.String(100))
    siret = db.Column(db.String(20))
    activite_principale = db.Column(db.String(200))
    produit_principal = db.Column(db.String(200))
    marche_principal = db.Column(db.String(200))
    systeme_production = db.Column(db.String(200))
    possede_marque = db.Column(db.Boolean, default=False)
    marque_client = db.Column(db.String(100))
    licence = db.Column(db.String(100))
    pays = db.Column(db.String(100))
    departement = db.Column(db.String(100))
    ville = db.Column(db.String(100))
    code_postal = db.Column(db.String(10))
    rue = db.Column(db.String(200))
    contact_nom = db.Column(db.String(100))
    contact_prenom = db.Column(db.String(100))
    contact_fonction = db.Column(db.String(100))
    contact_gsm = db.Column(db.String(20))
    contact_telephone = db.Column(db.String(20))
    contact_email = db.Column(db.String(120))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Fournisseur {self.nom}>'

@app.route('/')
def login():
        
    return redirect(url_for('index'))

@app.route('/home')
def index():
    stats = {
        'total_fournisseurs': Fournisseur.query.count(),
        'nombre_pays': 2,
        'updates_recents': 5,
    }
    return render_template('index.html', stats=stats)



@app.route('/fournisseur')
def fournisseur():
    # Exemple de données récupérées depuis une base de données ou calculées
    stats = {
        'total_fournisseurs': 150,
        'nombre_pays': 12,
        'updates_recents': "Mise à jour il y a 2 jours"
    }
    
    activites_recentes = [
        {
            'date': '2025-02-20',
            'fournisseur_id': 1,
            'fournisseur_nom': 'Fournisseur A',
            'action': 'Ajouté'
        },
        {
            'date': '2025-02-21',
            'fournisseur_id': 2,
            'fournisseur_nom': 'Fournisseur B',
            'action': 'Modifié'
        }
    ]
    
    # Passage des variables à votre template index.html
    return render_template('liste.html', stats=stats, activites_recentes=activites_recentes)



@app.route('/administration')
def administration():
    stats = {
        'total_fournisseurs': Fournisseur.query.count(),
        'nombre_pays': 2,
        'updates_recents': 5,
    }
    return render_template('administration.html',stats=stats)

# New route to trigger scraping
@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        urls = request.form.get('urls').split('\n')
        urls = [url.strip() for url in urls if url.strip()]
        
        # Launch async scraping tasks
        tasks = [scrape_async.delay(url) for url in urls]
        
        # Store task IDs in session for status checking
        task_ids = [task.id for task in tasks]
        return jsonify({'message': 'Scraping started', 'task_ids': task_ids})
    
    return render_template('scrape.html')

@app.route('/task_status/<task_id>')
def task_status(task_id):
    task = scrape_async.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state == 'SUCCESS':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return jsonify(response)

# Celery task for scraping
@celery.task(name='app.scrape_async')
def scrape_async(url):
    return scrape_company_details(url)

import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from flask import jsonify, send_file
import os
from a import scrape_data  # Import de la fonction


@app.route("/scrap_site", methods=["GET", "POST"])
def scrap_site():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("scrap_site.html", error="Veuillez entrer une URL.")
        
        try:
            data = scrape_data(url)
            return render_template("scrap_site.html", data=data)
        except Exception as e:
            return render_template("scrap_site.html", error=str(e))

    return render_template("scrap_site.html")
# Route pour rechercher des fournisseurs
@app.route('/recherche-fournisseurs', methods=['GET', 'POST'])
def recherche_fournisseurs():
    if request.method == 'POST':
        pays = request.form.get('pays')
        departement = request.form.get('departement')
        famille_produit = request.form.get('famille_produit')
        
        # Filtrage des fournisseurs en fonction des critères
        fournisseurs = Fournisseur.query.filter_by(
            pays=pays,
            departement=departement,
            micro_famille=famille_produit
        ).all()
        
        return render_template('resultat_recherche.html', fournisseurs=fournisseurs)
    
    return render_template('recherche_fournisseur.html')

# Route pour afficher les détails d'un fournisseur
@app.route('/details-fournisseur/<int:id>')
def details_fournisseur(id):
    fournisseur = Fournisseur.query.get_or_404(id)
    return render_template('details_fournisseurs.html', fournisseur=fournisseur)

# Route pour vérifier l'existence de fournisseurs
@app.route('/verifier-existence', methods=['POST'])
def verifier_existence():
    fournisseurs = request.json.get('fournisseurs', [])
    resultats = {
        'existants': [],
        'non_existants': []
    }
    
    for fournisseur in fournisseurs:
        existe = Fournisseur.query.filter_by(nom=fournisseur).first()
        if existe:
            resultats['existants'].append(fournisseur)
        else:
            resultats['non_existants'].append(fournisseur)
    
    return jsonify(resultats)



# Route pour mettre à jour un fournisseur
@app.route('/mise-a-jour-crm/<int:id>', methods=['GET', 'POST'])
def mise_a_jour_crm(id):
    fournisseur = Fournisseur.query.get_or_404(id)
    
    if request.method == 'POST':
        # Mise à jour des champs du fournisseur
        fournisseur.nom = request.form.get('nom')
        fournisseur.telephone = request.form.get('telephone')
        fournisseur.mobile = request.form.get('mobile')
        fournisseur.email = request.form.get('email')
        fournisseur.site_web = request.form.get('site_web')
        # Mettre à jour tous les autres champs...
        
        db.session.commit()
        print('Fournisseur mis à jour avec succès!', 'success')
        return redirect(url_for('details_fournisseur', id=id))
    
    return render_template('mise_a_jour_crm.html', fournisseur=fournisseur)

# Route pour ajouter un nouveau fournisseur
@app.route('/ajouter-fournisseur', methods=['GET', 'POST'])
def ajouter_fournisseur():
    if request.method == 'POST':
        # Création d'un nouveau fournisseur
        nouveau_fournisseur = Fournisseur(
            nom=request.form.get('nom'),
            telephone=request.form.get('telephone'),
            mobile=request.form.get('mobile'),
            email=request.form.get('email'),
            site_web=request.form.get('site_web'),
            # Ajouter tous les autres champs...
        )
        
        db.session.add(nouveau_fournisseur)
        db.session.commit()
        print('Nouveau fournisseur ajouté avec succès!', 'success')
        return redirect(url_for('details_fournisseur', id=nouveau_fournisseur.id))
    
    return render_template('ajouter_fournisseur.html')

# Routes API
@app.route('/api/fournisseurs', methods=['GET'])
def api_liste_fournisseurs():
    fournisseurs = Fournisseur.query.all()
    return jsonify([{
        'id': f.id,
        'nom': f.nom,
        'pays': f.pays,
        'ville': f.ville,
        'produit_principal': f.produit_principal
    } for f in fournisseurs])

@app.route('/api/fournisseur/<int:id>', methods=['GET'])
def api_details_fournisseur(id):
    fournisseur = Fournisseur.query.get_or_404(id)
    return jsonify({
        'id': fournisseur.id,
        'nom': fournisseur.nom,
        'telephone': fournisseur.telephone,
        'email': fournisseur.email,
        # Autres champs...
    })

# Point d'entrée de l'application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables de la base de données si elles n'existent pas
    app.run(debug=True)  # Lance l'application en mode debug