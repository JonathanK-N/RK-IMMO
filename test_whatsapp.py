#!/usr/bin/env python3
"""
Script de test pour la fonctionnalité WhatsApp
"""

import urllib.parse
from datetime import datetime

def test_whatsapp_message_generation():
    """Test de génération de message WhatsApp"""
    
    # Données de test
    contact_data = {
        'name': 'Jean Dupont',
        'email': 'jean.dupont@email.com',
        'phone': '01 23 45 67 89',
        'subject': 'Demande d\'information',
        'message': 'Je suis intéressé par vos services immobiliers.'
    }
    
    property_info = {
        'id': 1,
        'title': 'Magnifique Appartement Haussmannien - Paris 16ème',
        'price': 1250000,
        'surface': 120,
        'city': 'Paris'
    }
    
    # Génération du message
    message_parts = [
        "🏠 *NOUVEAU CONTACT RK IMMO*",
        "",
        f"👤 *Nom:* {contact_data['name']}",
        f"📧 *Email:* {contact_data['email']}",
        f"📱 *Téléphone:* {contact_data['phone']}",
        f"📋 *Sujet:* {contact_data['subject']}",
        f"💬 *Message:* {contact_data['message']}",
        "",
        "🏡 *BIEN CONCERNÉ:*",
        f"📍 *Titre:* {property_info['title']}",
        f"💰 *Prix:* {property_info['price']:,.0f} €",
        f"📐 *Surface:* {property_info['surface']} m²",
        f"🏙️ *Ville:* {property_info['city']}",
        f"🔗 *Lien:* http://localhost:5000/property/{property_info['id']}",
        "",
        f"⏰ *Date:* {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
        "",
        "_Message automatique de RK IMMO_"
    ]
    
    message = "\n".join(message_parts)
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/243842465238?text={encoded_message}"
    
    print("=== TEST GENERATION MESSAGE WHATSAPP ===")
    print("\n[MSG] Message genere:")
    print(message)
    print(f"\n[URL] URL WhatsApp generee:")
    print(whatsapp_url)
    print(f"\n[OK] Longueur du message: {len(message)} caracteres")
    print(f"[OK] Longueur de l'URL: {len(whatsapp_url)} caracteres")
    
    # Vérifications
    assert "RK IMMO" in message
    assert contact_data['name'] in message
    assert contact_data['email'] in message
    assert property_info['title'] in message
    assert "243842465238" in whatsapp_url
    
    print("[OK] Tous les tests sont passes!")
    
    return whatsapp_url

def test_simple_whatsapp_message():
    """Test de message WhatsApp simple"""
    
    simple_message = "🏠 Bonjour RK IMMO, j'aimerais avoir des informations sur vos services immobiliers."
    encoded_message = urllib.parse.quote(simple_message)
    whatsapp_url = f"https://wa.me/243842465238?text={encoded_message}"
    
    print("\n=== TEST MESSAGE SIMPLE ===")
    print(f"[MSG] Message: {simple_message}")
    print(f"[URL] URL: {whatsapp_url}")
    
    return whatsapp_url

def test_visit_request_message():
    """Test de message pour demande de visite"""
    
    property_title = "Magnifique Appartement Haussmannien - Paris 16ème"
    property_url = "http://localhost:5000/property/1"
    
    message = f"""🏠 *DEMANDE DE VISITE - RK IMMO*

📋 *Bien:* {property_title}
🔗 *Lien:* {property_url}

📅 Je souhaiterais planifier une visite pour ce bien. Quand seriez-vous disponible ?

_Message depuis le site RK IMMO_"""
    
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/243842465238?text={encoded_message}"
    
    print("\n=== TEST DEMANDE DE VISITE ===")
    print(f"[MSG] Message: {message}")
    print(f"[URL] URL: {whatsapp_url}")
    
    return whatsapp_url

if __name__ == '__main__':
    print("[TEST] TESTS FONCTIONNALITE WHATSAPP RK IMMO")
    print("=" * 50)
    
    try:
        # Test 1: Message complet avec propriété
        url1 = test_whatsapp_message_generation()
        
        # Test 2: Message simple
        url2 = test_simple_whatsapp_message()
        
        # Test 3: Demande de visite
        url3 = test_visit_request_message()
        
        print("\n" + "=" * 50)
        print("[SUCCESS] TOUS LES TESTS SONT REUSSIS!")
        print("\n[URLS] URLs generees:")
        print(f"1. Contact complet: {url1[:100]}...")
        print(f"2. Message simple: {url2[:100]}...")
        print(f"3. Demande visite: {url3[:100]}...")
        
        print("\n[INFO] Instructions:")
        print("1. Copiez une des URLs ci-dessus")
        print("2. Collez-la dans votre navigateur")
        print("3. WhatsApp s'ouvrira avec le message pre-rempli")
        print("4. Vous pourrez envoyer le message directement")
        
    except Exception as e:
        print(f"[ERROR] Erreur lors des tests: {e}")
        raise