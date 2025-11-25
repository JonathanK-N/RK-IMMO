#!/usr/bin/env python3
"""
Script d'initialisation de la base de données RK IMMO
Crée les tables et ajoute des données d'exemple
"""

from app import app, db, User, Property, Contact
from werkzeug.security import generate_password_hash
import json

def init_database():
    """Initialise la base de données avec des données d'exemple"""
    
    with app.app_context():
        # Supprimer toutes les tables existantes
        db.drop_all()
        
        # Créer toutes les tables
        db.create_all()
        
        # Créer un utilisateur admin
        admin = User(
            username='admin',
            email='admin@rk-immo.fr',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        
        # Créer des propriétés d'exemple
        properties_data = [
            {
                'title': 'Magnifique Villa Moderne - Gombe, Kinshasa',
                'description': 'Superbe villa de 250m² située dans le quartier résidentiel de Gombe. Composée de 5 pièces avec de beaux volumes, finitions modernes, jardin paysager et vue sur le fleuve Congo. Proche des ambassades et centres d\'affaires.',
                'price': 350000,
                'property_type': 'Vente',
                'category': 'Maison',
                'bedrooms': 4,
                'bathrooms': 3,
                'surface': 250,
                'city': 'Kinshasa',
                'address': 'Avenue des Ambassades, Gombe',
                'images': json.dumps([
                    'https://images.unsplash.com/photo-1564013799919-ab600027ffc6',
                    'https://images.unsplash.com/photo-1586023492125-27b2c045efd7',
                    'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2'
                ]),
                'featured': True,
                'available': True
            },
            {
                'title': 'Résidence de Luxe avec Piscine - Limete, Kinshasa',
                'description': 'Villa d\'architecte de 300m² sur un terrain de 1000m². 6 chambres, 4 salles de bains, piscine, garage double, générateur. Quartier résidentiel sécurisé avec gardiennage 24h/24.',
                'price': 280000,
                'property_type': 'Vente',
                'category': 'Maison',
                'bedrooms': 6,
                'bathrooms': 4,
                'surface': 300,
                'city': 'Kinshasa',
                'address': 'Avenue Lumumba, Limete',
                'images': json.dumps([
                    'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9',
                    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c',
                    'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3'
                ]),
                'featured': True,
                'available': True
            },
            {
                'title': 'Appartement Moderne - Bandalungwa, Kinshasa',
                'description': 'Charmant appartement de 80m² entièrement rénové dans le quartier de Bandalungwa. Cuisine équipée, 2 salles de bain modernes, balcon, proche marché central et transports.',
                'price': 450,
                'property_type': 'Location',
                'category': 'Appartement',
                'bedrooms': 2,
                'bathrooms': 2,
                'surface': 80,
                'city': 'Kinshasa',
                'address': 'Avenue Kasongo, Bandalungwa',
                'images': json.dumps([
                    'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267',
                    'https://images.unsplash.com/photo-1560448075-bb485b067938',
                    'https://images.unsplash.com/photo-1560449752-c4b8b5c6b9c8'
                ]),
                'featured': False,
                'available': True
            },
            {
                'title': 'Bureaux Standing - Centre-ville, Kinshasa',
                'description': 'Plateau de bureaux de 200m² dans immeuble moderne au centre-ville. Open space modulable, salle de réunion, kitchenette, générateur, parking sécurisé inclus.',
                'price': 1200,
                'property_type': 'Location',
                'category': 'Bureau',
                'bedrooms': 0,
                'bathrooms': 2,
                'surface': 200,
                'city': 'Kinshasa',
                'address': 'Boulevard du 30 Juin, Gombe',
                'images': json.dumps([
                    'https://images.unsplash.com/photo-1497366216548-37526070297c',
                    'https://images.unsplash.com/photo-1497366754035-f200968a6e72',
                    'https://images.unsplash.com/photo-1497366412874-3415097a27e7'
                ]),
                'featured': True,
                'available': True
            },
            {
                'title': 'Appartement Familial - Lemba, Kinshasa',
                'description': 'Bel appartement de 120m² avec balcon, 4 pièces lumineuses, cuisine moderne, proche université de Kinshasa. Idéal famille, quartier calme et sécurisé.',
                'price': 85000,
                'property_type': 'Vente',
                'category': 'Appartement',
                'bedrooms': 3,
                'bathrooms': 2,
                'surface': 120,
                'city': 'Kinshasa',
                'address': 'Avenue de l\'Université, Lemba',
                'images': json.dumps([
                    'https://images.unsplash.com/photo-1484154218962-a197022b5858',
                    'https://images.unsplash.com/photo-1493809842364-78817add7ffb',
                    'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688'
                ]),
                'featured': False,
                'available': True
            },
            {
                'title': 'Duplex Moderne - Ngaliema, Kinshasa',
                'description': 'Duplex atypique de 180m² dans résidence moderne. Hauteur sous plafond 4m, grandes baies vitrées, mezzanine, terrasse avec vue sur le fleuve Congo.',
                'price': 800,
                'property_type': 'Location',
                'category': 'Appartement',
                'bedrooms': 3,
                'bathrooms': 2,
                'surface': 180,
                'city': 'Kinshasa',
                'address': 'Avenue Ngaliema, Mont Ngafula',
                'images': json.dumps([
                    'https://images.unsplash.com/photo-1586023492125-27b2c045efd7',
                    'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2',
                    'https://images.unsplash.com/photo-1484154218962-a197022b5858'
                ]),
                'featured': True,
                'available': True
            },
            {
                'title': 'Maison Familiale - Matete, Kinshasa',
                'description': 'Charmante maison familiale de 160m² avec grand jardin. 5 pièces, garage, citerne d\'eau, proche marché de Matete et écoles.',
                'price': 95000,
                'property_type': 'Vente',
                'category': 'Maison',
                'bedrooms': 4,
                'bathrooms': 2,
                'surface': 160,
                'city': 'Kinshasa',
                'address': 'Avenue Matete, Commune de Matete',
                'images': json.dumps([
                    'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9',
                    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c',
                    'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3'
                ]),
                'featured': False,
                'available': True
            },
            {
                'title': 'Penthouse de Luxe - Ma Campagne, Kinshasa',
                'description': 'Exceptionnel penthouse de 220m² avec terrasse de 80m². Vue panoramique sur Kinshasa, prestations haut de gamme, ascenseur privé, générateur de secours.',
                'price': 180000,
                'property_type': 'Vente',
                'category': 'Appartement',
                'bedrooms': 4,
                'bathrooms': 3,
                'surface': 220,
                'city': 'Kinshasa',
                'address': 'Avenue Ma Campagne, Ngiri-Ngiri',
                'images': json.dumps([
                    'https://images.unsplash.com/photo-1564013799919-ab600027ffc6',
                    'https://images.unsplash.com/photo-1586023492125-27b2c045efd7',
                    'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2'
                ]),
                'featured': True,
                'available': True
            },
            {
                'title': 'Villa Moderne - Lubumbashi, Haut-Katanga',
                'description': 'Belle villa de 200m² dans le quartier résidentiel de Lubumbashi. 4 chambres, 3 salles de bains, jardin, garage, générateur. Proche centre-ville et université.',
                'price': 120000,
                'property_type': 'Vente',
                'category': 'Maison',
                'bedrooms': 4,
                'bathrooms': 3,
                'surface': 200,
                'city': 'Lubumbashi',
                'address': 'Avenue Mobutu, Quartier Golf',
                'images': json.dumps([
                    'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9',
                    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c',
                    'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3'
                ]),
                'featured': False,
                'available': True
            },
            {
                'title': 'Appartement Standing - Bukavu, Sud-Kivu',
                'description': 'Appartement de 100m² avec vue sur le lac Kivu. 3 chambres, 2 salles de bains, balcon, proche marché central. Quartier sécurisé et calme.',
                'price': 600,
                'property_type': 'Location',
                'category': 'Appartement',
                'bedrooms': 3,
                'bathrooms': 2,
                'surface': 100,
                'city': 'Bukavu',
                'address': 'Avenue P.E. Lumumba, Centre-ville',
                'images': json.dumps([
                    'https://images.unsplash.com/photo-1484154218962-a197022b5858',
                    'https://images.unsplash.com/photo-1493809842364-78817add7ffb',
                    'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688'
                ]),
                'featured': False,
                'available': True
            },
            {
                'title': 'Maison Familiale - Goma, Nord-Kivu',
                'description': 'Maison familiale de 150m² dans un quartier résidentiel de Goma. 4 chambres, 2 salles de bains, jardin, vue sur le volcan Nyiragongo. Proche écoles internationales.',
                'price': 80000,
                'property_type': 'Vente',
                'category': 'Maison',
                'bedrooms': 4,
                'bathrooms': 2,
                'surface': 150,
                'city': 'Goma',
                'address': 'Avenue des Volcans, Quartier Himbi',
                'images': json.dumps([
                    'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9',
                    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c',
                    'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3'
                ]),
                'featured': False,
                'available': True
            }
        ]
        
        for prop_data in properties_data:
            property = Property(**prop_data)
            db.session.add(property)
        
        # Créer quelques contacts d'exemple
        contacts_data = [
            {
                'name': 'Marie Kabongo',
                'email': 'marie.kabongo@gmail.com',
                'phone': '+243 81 234 56 78',
                'subject': 'Demande de visite',
                'message': 'Bonjour, je suis intéressée par la villa moderne à Gombe. Pourriez-vous organiser une visite cette semaine ?',
                'property_id': 1
            },
            {
                'name': 'Jean-Pierre Mukendi',
                'email': 'jp.mukendi@yahoo.fr',
                'phone': '+243 82 345 67 89',
                'subject': 'Estimation de bien',
                'message': 'Je souhaiterais faire estimer ma maison à Lemba. Pouvez-vous me contacter pour convenir d\'un rendez-vous ?'
            },
            {
                'name': 'Grace Mbuyi',
                'email': 'grace.mbuyi@hotmail.com',
                'phone': '+243 83 456 78 90',
                'subject': 'Recherche appartement',
                'message': 'Je recherche un appartement 3 pièces à Kinshasa, budget 100k USD. Merci de me tenir informée de vos nouveautés.'
            }
        ]
        
        for contact_data in contacts_data:
            contact = Contact(**contact_data)
            db.session.add(contact)
        
        # Sauvegarder toutes les données
        db.session.commit()
        
        print("[OK] Base de donnees initialisee avec succes!")
        print(f"[OK] {len(properties_data)} proprietes ajoutees")
        print(f"[OK] {len(contacts_data)} contacts ajoutes")
        print("[OK] Utilisateur admin cree (admin/admin123)")

if __name__ == '__main__':
    init_database()