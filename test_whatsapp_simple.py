#!/usr/bin/env python3
"""
Script de test simple pour la fonctionnalité WhatsApp (sans emojis)
"""

import urllib.parse
from datetime import datetime

def test_whatsapp_message_generation():
    """Test de génération de message WhatsApp"""
    
    # Données de test
    contact_data = {
        'name': 'Jean-Pierre Mukendi',
        'email': 'jp.mukendi@gmail.com',
        'phone': '+243 81 234 56 78',
        'subject': 'Demande d\'information',
        'message': 'Je suis intéressé par vos services immobiliers à Kinshasa.'
    }
    
    property_info = {
        'id': 1,
        'title': 'Magnifique Villa Moderne - Gombe, Kinshasa',
        'price': 350000,
        'surface': 250,
        'city': 'Kinshasa'
    }
    
    # Génération du message (version ASCII)
    message_parts = [
        "*** NOUVEAU CONTACT RK IMMO ***",
        "",
        f"Nom: {contact_data['name']}",
        f"Email: {contact_data['email']}",
        f"Telephone: {contact_data['phone']}",
        f"Sujet: {contact_data['subject']}",
        f"Message: {contact_data['message']}",
        "",
        "BIEN CONCERNE:",
        f"Titre: {property_info['title']}",
        f"Prix: {property_info['price']:,.0f} euros",
        f"Surface: {property_info['surface']} m2",
        f"Ville: {property_info['city']}",
        f"Lien: http://localhost:5000/property/{property_info['id']}",
        "",
        f"Date: {datetime.now().strftime('%d/%m/%Y a %H:%M')}",
        "",
        "Message automatique de RK IMMO"
    ]
    
    message = "\n".join(message_parts)
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://wa.me/243842465238?text={encoded_message}"
    
    print("=== TEST GENERATION MESSAGE WHATSAPP ===")
    print("\nMessage genere:")
    print(message)
    print(f"\nURL WhatsApp generee:")
    print(whatsapp_url)
    print(f"\nLongueur du message: {len(message)} caracteres")
    print(f"Longueur de l'URL: {len(whatsapp_url)} caracteres")
    
    # Vérifications
    assert "RK IMMO" in message
    assert contact_data['name'] in message
    assert contact_data['email'] in message
    assert property_info['title'] in message
    assert "243842465238" in whatsapp_url
    
    print("Tous les tests sont passes!")
    
    return whatsapp_url

def test_simple_whatsapp_message():
    """Test de message WhatsApp simple"""
    
    simple_message = "Bonjour RK IMMO, j'aimerais avoir des informations sur vos services immobiliers à Kinshasa."
    encoded_message = urllib.parse.quote(simple_message)
    whatsapp_url = f"https://wa.me/243842465238?text={encoded_message}"
    
    print("\n=== TEST MESSAGE SIMPLE ===")
    print(f"Message: {simple_message}")
    print(f"URL: {whatsapp_url}")
    
    return whatsapp_url

if __name__ == '__main__':
    print("TESTS FONCTIONNALITE WHATSAPP RK IMMO")
    print("=" * 50)
    
    try:
        # Test 1: Message complet avec propriété
        url1 = test_whatsapp_message_generation()
        
        # Test 2: Message simple
        url2 = test_simple_whatsapp_message()
        
        print("\n" + "=" * 50)
        print("TOUS LES TESTS SONT REUSSIS!")
        print("\nURLs generees:")
        print(f"1. Contact complet: {url1[:100]}...")
        print(f"2. Message simple: {url2[:100]}...")
        
        print("\nInstructions:")
        print("1. Copiez une des URLs ci-dessus")
        print("2. Collez-la dans votre navigateur")
        print("3. WhatsApp s'ouvrira avec le message pre-rempli")
        print("4. Vous pourrez envoyer le message directement")
        print(f"5. Le message sera envoye au numero: +243 84 24 65 238")
        
    except Exception as e:
        print(f"Erreur lors des tests: {e}")
        raise