#!/usr/bin/env python3
"""
Script de démarrage pour l'application RK IMMO
Usage: python run.py
"""

import os
import sys
from app import app, create_tables

def main():
    """Fonction principale pour démarrer l'application"""
    
    # Initialiser la base de données
    print("🔧 Initialisation de la base de données...")
    create_tables()
    print("✅ Base de données initialisée avec succès!")
    
    # Configuration pour le développement
    app.config['DEBUG'] = True
    
    # Port par défaut
    port = int(os.environ.get('PORT', 5000))
    
    print(f"""
🚀 Démarrage de RK IMMO...

📍 Application disponible sur:
   - Local: http://localhost:{port}
   - Réseau: http://0.0.0.0:{port}

👨💼 Interface d'administration:
   - URL: http://localhost:{port}/admin/proprietes
   - Utilisateur: admin
   - Mot de passe: password

🛑 Appuyez sur Ctrl+C pour arrêter le serveur
    """)
    
    try:
        app.run(
            host='0.0.0.0',
            port=port,
            debug=True,
            use_reloader=True
        )
    except KeyboardInterrupt:
        print("\n👋 Arrêt du serveur...")
        sys.exit(0)

if __name__ == '__main__':
    main()