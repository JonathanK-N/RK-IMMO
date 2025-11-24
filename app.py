from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import db, Propriete, Reservation
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

def create_tables():
    with app.app_context():
        db.create_all()
        # Ajouter des données de démonstration
        if Propriete.query.count() == 0:
            demo_properties = [
            Propriete(
                titre="Villa Moderne avec Piscine",
                description="Magnifique villa contemporaine avec piscine privée, jardin paysager et vue panoramique.",
                prix=450000,
                localisation="Gombe, Kinshasa",
                chambres=4,
                salles_bain=3,
                type_propriete="Villa",
                surface=250,
                images="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9,https://images.unsplash.com/photo-1600607687939-ce8a6c25118c,https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3"
            ),
            Propriete(
                titre="Appartement Centre-Ville",
                description="Appartement moderne au cœur de la ville, proche de tous les services.",
                prix=280000,
                localisation="Limete, Kinshasa",
                chambres=2,
                salles_bain=2,
                type_propriete="Appartement",
                surface=85,
                images="https://images.unsplash.com/photo-1522708323590-d24dbb6b0267,https://images.unsplash.com/photo-1560448204-e02f11c3d0e2"
            ),
            Propriete(
                titre="Maison Familiale",
                description="Parfaite pour une famille, avec grand jardin et garage double.",
                prix=320000,
                localisation="Bandalungwa, Kinshasa",
                chambres=3,
                salles_bain=2,
                type_propriete="Maison",
                surface=180,
                images="https://images.unsplash.com/photo-1570129477492-45c003edd2be,https://images.unsplash.com/photo-1588880331179-bc9b93a8cb5e"
            )
            ]
            for prop in demo_properties:
                db.session.add(prop)
            db.session.commit()

# Routes Frontend
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proprietes')
def proprietes():
    return render_template('proprietes.html')

@app.route('/propriete/<int:id>')
def propriete_detail(id):
    return render_template('propriete_detail.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# API Routes
@app.route('/api/properties')
def get_properties():
    prix_min = request.args.get('prix_min', type=float)
    prix_max = request.args.get('prix_max', type=float)
    localisation = request.args.get('localisation')
    type_propriete = request.args.get('type')
    
    query = Propriete.query
    
    if prix_min:
        query = query.filter(Propriete.prix >= prix_min)
    if prix_max:
        query = query.filter(Propriete.prix <= prix_max)
    if localisation:
        query = query.filter(Propriete.localisation.contains(localisation))
    if type_propriete:
        query = query.filter(Propriete.type_propriete == type_propriete)
    
    properties = query.all()
    return jsonify([prop.to_dict() for prop in properties])

@app.route('/api/properties/<int:id>')
def get_property(id):
    propriete = Propriete.query.get_or_404(id)
    return jsonify(propriete.to_dict())

@app.route('/api/reservation', methods=['POST'])
def create_reservation():
    data = request.get_json()
    
    try:
        reservation = Reservation(
            propriete_id=data['propriete_id'],
            nom_client=data['nom_client'],
            email=data['email'],
            telephone=data['telephone'],
            type_demande=data['type_demande'],
            message=data.get('message', '')
        )
        
        db.session.add(reservation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Demande envoyée avec succès!'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erreur lors de l\'envoi de la demande'
        }), 400

# Admin basique
@app.route('/admin/proprietes')
def admin_proprietes():
    # Authentification basique (à améliorer en production)
    auth = request.authorization
    if not auth or auth.username != 'admin' or auth.password != 'password':
        return '', 401, {'WWW-Authenticate': 'Basic realm="Admin"'}
    
    proprietes = Propriete.query.all()
    reservations = Reservation.query.all()
    return render_template('admin.html', proprietes=proprietes, reservations=reservations)

if __name__ == '__main__':
    create_tables()  # Initialiser la base de données
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)