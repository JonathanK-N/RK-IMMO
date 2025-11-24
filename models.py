from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Propriete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    prix = db.Column(db.Float, nullable=False)
    localisation = db.Column(db.String(200), nullable=False)
    chambres = db.Column(db.Integer, nullable=False)
    salles_bain = db.Column(db.Integer, nullable=False)
    images = db.Column(db.Text)  # URLs séparées par des virgules
    statut = db.Column(db.String(20), default='Disponible')
    type_propriete = db.Column(db.String(50), nullable=False)
    surface = db.Column(db.Float)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'prix': self.prix,
            'localisation': self.localisation,
            'chambres': self.chambres,
            'salles_bain': self.salles_bain,
            'images': self.images.split(',') if self.images else [],
            'statut': self.statut,
            'type_propriete': self.type_propriete,
            'surface': self.surface
        }

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    propriete_id = db.Column(db.Integer, db.ForeignKey('propriete.id'), nullable=False)
    nom_client = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    type_demande = db.Column(db.String(20), nullable=False)  # 'Visite' ou 'Ferme'
    message = db.Column(db.Text)
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)
    
    propriete = db.relationship('Propriete', backref=db.backref('reservations', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'propriete_id': self.propriete_id,
            'nom_client': self.nom_client,
            'email': self.email,
            'telephone': self.telephone,
            'type_demande': self.type_demande,
            'message': self.message,
            'date_demande': self.date_demande.isoformat()
        }