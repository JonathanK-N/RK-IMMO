#!/usr/bin/env python3
"""
Script pour ajouter des données d'exemple à la base de données existante
"""

import os
from app import app, db, Property
import json

def add_sample_properties():
    """Ajoute des propriétés d'exemple si la base est vide"""
    
    with app.app_context():
        # Vérifier si des propriétés existent déjà
        existing_count = Property.query.count()
        if existing_count > 0:
            print(f"[INFO] {existing_count} propriétés déjà présentes")
            return
        
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
            }
        ]
        
        for prop_data in properties_data:
            property = Property(**prop_data)
            db.session.add(property)
        
        db.session.commit()
        print(f"[OK] {len(properties_data)} propriétés ajoutées avec succès!")

if __name__ == '__main__':
    add_sample_properties()