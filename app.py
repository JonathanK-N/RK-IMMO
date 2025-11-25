from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import json
import urllib.parse

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rk-immo-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rk_immo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Configuration WhatsApp
WHATSAPP_NUMBER = '+243842465238'  # Votre numéro WhatsApp

db = SQLAlchemy(app)

# Modèles de base de données
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    property_type = db.Column(db.String(50), nullable=False)  # Vente, Location
    category = db.Column(db.String(50), nullable=False)  # Appartement, Maison, Bureau
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    surface = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    images = db.Column(db.Text)  # JSON string des images
    featured = db.Column(db.Boolean, default=False)
    available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes principales
@app.route('/')
def index():
    featured_properties = Property.query.filter_by(featured=True, available=True).limit(6).all()
    return render_template('index.html', properties=featured_properties)

@app.route('/properties')
def properties():
    page = request.args.get('page', 1, type=int)
    property_type = request.args.get('type', '')
    category = request.args.get('category', '')
    city = request.args.get('city', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    bedrooms = request.args.get('bedrooms', type=int)
    
    query = Property.query.filter_by(available=True)
    
    if property_type:
        query = query.filter_by(property_type=property_type)
    if category:
        query = query.filter_by(category=category)
    if city:
        query = query.filter(Property.city.contains(city))
    if min_price:
        query = query.filter(Property.price >= min_price)
    if max_price:
        query = query.filter(Property.price <= max_price)
    if bedrooms:
        query = query.filter_by(bedrooms=bedrooms)
    
    properties = query.paginate(page=page, per_page=9, error_out=False)
    cities = db.session.query(Property.city).distinct().all()
    
    return render_template('properties.html', properties=properties, cities=[c[0] for c in cities])

@app.route('/property/<int:id>')
def property_detail(id):
    property = Property.query.get_or_404(id)
    similar_properties = Property.query.filter(
        Property.category == property.category,
        Property.id != property.id,
        Property.available == True
    ).limit(3).all()
    
    return render_template('property_detail.html', property=property, similar_properties=similar_properties)

def send_whatsapp_notification(contact_data, property_info=None):
    """Génère un lien WhatsApp avec les détails du contact"""
    message_parts = [
        "🏠 *NOUVEAU CONTACT RK IMMO*",
        "",
        f"👤 *Nom:* {contact_data['name']}",
        f"📧 *Email:* {contact_data['email']}",
    ]
    
    if contact_data.get('phone'):
        message_parts.append(f"📱 *Téléphone:* {contact_data['phone']}")
    
    message_parts.extend([
        f"📋 *Sujet:* {contact_data['subject']}",
        f"💬 *Message:* {contact_data['message']}",
        ""
    ])
    
    if property_info:
        message_parts.extend([
            "🏡 *BIEN CONCERNÉ:*",
            f"📍 *Titre:* {property_info.title}",
            f"💰 *Prix:* {property_info.price:,.0f} $",
            f"📐 *Surface:* {property_info.surface} m²",
            f"🏙️ *Ville:* {property_info.city}",
            f"🔗 *Lien:* {request.url_root}property/{property_info.id}",
            ""
        ])
    
    message_parts.extend([
        f"⏰ *Date:* {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
        "",
        "_Message automatique de RK IMMO_"
    ])
    
    message = "\n".join(message_parts)
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER.replace('+', '')}?text={encoded_message}"
    
    return whatsapp_url

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        contact_data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form.get('phone'),
            'subject': request.form['subject'],
            'message': request.form['message']
        }
        
        # Créer l'enregistrement de contact
        contact = Contact(
            name=contact_data['name'],
            email=contact_data['email'],
            phone=contact_data['phone'],
            subject=contact_data['subject'],
            message=contact_data['message'],
            property_id=request.form.get('property_id', type=int)
        )
        db.session.add(contact)
        db.session.commit()
        
        # Récupérer les infos du bien si spécifié
        property_info = None
        if contact.property_id:
            property_info = Property.query.get(contact.property_id)
        
        # Générer le lien WhatsApp
        whatsapp_url = send_whatsapp_notification(contact_data, property_info)
        
        flash('Votre message a été envoyé avec succès!', 'success')
        
        # Retourner la réponse avec le lien WhatsApp pour redirection automatique
        if request.headers.get('Content-Type') == 'application/json' or request.is_json:
            return jsonify({
                'success': True,
                'message': 'Message envoyé avec succès!',
                'whatsapp_url': whatsapp_url
            })
        
        # Pour les soumissions de formulaire normales, rediriger avec le lien en session
        session['whatsapp_redirect'] = whatsapp_url
        return redirect(url_for('contact'))
    
    # Récupérer le lien WhatsApp de la session s'il existe
    whatsapp_url = session.pop('whatsapp_redirect', None)
    
    return render_template('contact.html', whatsapp_url=whatsapp_url)

# Routes d'administration
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, is_admin=True).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['admin_id'] = user.id
            flash('Connexion réussie!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Identifiants incorrects!', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    flash('Déconnexion réussie!', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    total_properties = Property.query.count()
    available_properties = Property.query.filter_by(available=True).count()
    total_contacts = Contact.query.count()
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         total_properties=total_properties,
                         available_properties=available_properties,
                         total_contacts=total_contacts,
                         recent_contacts=recent_contacts)

@app.route('/admin/properties')
def admin_properties():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    page = request.args.get('page', 1, type=int)
    properties = Property.query.paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/properties.html', properties=properties)

@app.route('/admin/property/add', methods=['GET', 'POST'])
def admin_add_property():
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        property = Property(
            title=request.form['title'],
            description=request.form['description'],
            price=float(request.form['price']),
            property_type=request.form['property_type'],
            category=request.form['category'],
            bedrooms=int(request.form['bedrooms']),
            bathrooms=int(request.form['bathrooms']),
            surface=float(request.form['surface']),
            city=request.form['city'],
            address=request.form['address'],
            images=request.form.get('images', '[]'),
            featured=bool(request.form.get('featured')),
            available=bool(request.form.get('available', True))
        )
        db.session.add(property)
        db.session.commit()
        flash('Propriété ajoutée avec succès!', 'success')
        return redirect(url_for('admin_properties'))
    
    return render_template('admin/add_property.html')

# API pour envoyer un message WhatsApp
@app.route('/api/send-whatsapp', methods=['POST'])
def api_send_whatsapp():
    data = request.get_json()
    
    # Validation des données
    required_fields = ['name', 'email', 'subject', 'message']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'Le champ {field} est requis'}), 400
    
    # Créer l'enregistrement de contact
    contact = Contact(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        subject=data['subject'],
        message=data['message'],
        property_id=data.get('property_id', type=int)
    )
    db.session.add(contact)
    db.session.commit()
    
    # Récupérer les infos du bien si spécifié
    property_info = None
    if contact.property_id:
        property_info = Property.query.get(contact.property_id)
    
    # Générer le lien WhatsApp
    whatsapp_url = send_whatsapp_notification(data, property_info)
    
    return jsonify({
        'success': True,
        'message': 'Contact enregistré avec succès!',
        'whatsapp_url': whatsapp_url
    })

# API pour le chatbot
@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    message = data.get('message', '').lower()
    
    responses = {
        'bonjour': 'Bonjour! Je suis l\'assistant virtuel de RK IMMO Kinshasa. Comment puis-je vous aider?',
        'horaires': 'Nos horaires sont du lundi au vendredi de 8h à 17h, et le samedi de 8h à 14h.',
        'contact': 'Vous pouvez nous contacter au +243 84 24 65 238, par email à info.rkimmo@gmail.com ou directement sur WhatsApp.',
        'whatsapp': 'Contactez-nous directement sur WhatsApp au +243 84 24 65 238 pour une réponse rapide!',
        'location': 'Pour louer un bien à Kinshasa, consultez notre catalogue et contactez-nous pour organiser une visite.',
        'achat': 'Pour acheter un bien à Kinshasa ou en RD Congo, notre équipe vous accompagne dans toutes les démarches.',
        'visite': 'Pour organiser une visite à Kinshasa, contactez-nous via le formulaire, appelez-nous ou écrivez-nous sur WhatsApp.',
        'prix': 'Les prix varient selon le quartier de Kinshasa et le type de bien. Consultez notre catalogue pour plus de détails.',
        'kinshasa': 'Nous sommes spécialisés dans l\'immobilier à Kinshasa: Gombe, Limete, Bandalungwa, Lemba, Ngaliema et autres communes.',
        'quartier': 'Nous couvrons tous les quartiers de Kinshasa: Gombe, Limete, Bandalungwa, Lemba, Ngaliema, Matete et bien d\'autres.',
        'agent': 'Pour parler directement à un agent, contactez-nous sur WhatsApp au +243 84 24 65 238',
        'default': 'Je ne comprends pas votre question. Voulez-vous parler à un de nos agents sur WhatsApp? Cliquez ici pour nous contacter: +243 84 24 65 238'
    }
    
    for key in responses:
        if key in message:
            response_text = responses[key]
            # Si la réponse contient une mention de WhatsApp, ajouter un bouton
            if 'whatsapp' in key.lower() or '+243' in response_text:
                return jsonify({
                    'response': response_text,
                    'whatsapp_button': True,
                    'whatsapp_url': 'https://wa.me/243842465238?text=Bonjour%20RK%20IMMO%2C%20j%27ai%20une%20question%20concernant%20vos%20services%20immobiliers.'
                })
            return jsonify({'response': response_text})
    
    return jsonify({
        'response': responses['default'],
        'whatsapp_button': True,
        'whatsapp_url': 'https://wa.me/243842465238?text=Bonjour%20RK%20IMMO%2C%20j%27ai%20une%20question%20concernant%20vos%20services%20immobiliers.'
    })

# Initialisation de la base de données
def create_tables():
    db.create_all()
    
    # Créer un admin par défaut
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@rk-immo.fr',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)