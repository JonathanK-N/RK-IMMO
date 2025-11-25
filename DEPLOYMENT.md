# 🚀 Déploiement Railway - RK IMMO

## Étapes de Déploiement

### 1. Préparer le Repository
```bash
git init
git add .
git commit -m "Initial commit - RK IMMO Kinshasa"
```

### 2. Pousser sur GitHub
```bash
git remote add origin https://github.com/VOTRE_USERNAME/rk-immo.git
git push -u origin main
```

### 3. Déployer sur Railway
1. Aller sur [railway.app](https://railway.app)
2. Se connecter avec GitHub
3. Cliquer "New Project"
4. Sélectionner "Deploy from GitHub repo"
5. Choisir votre repository `rk-immo`

### 4. Variables d'Environnement
Dans Railway Dashboard > Variables:
```
FLASK_ENV=production
SECRET_KEY=votre-cle-secrete-production
WHATSAPP_NUMBER=+243842465238
```

### 5. Domaine Personnalisé (Optionnel)
- Settings > Domains
- Ajouter votre domaine personnalisé

## URLs de Production
- **Site** : https://rk-immo-production.up.railway.app
- **Admin** : https://rk-immo-production.up.railway.app/admin/login

## Fichiers de Configuration
- ✅ `Procfile` - Commande de démarrage
- ✅ `requirements.txt` - Dépendances Python
- ✅ `railway.json` - Configuration Railway
- ✅ `runtime.txt` - Version Python
- ✅ `.gitignore` - Fichiers à ignorer

## Commandes Git
```bash
# Initialiser
git init
git add .
git commit -m "RK IMMO - Ready for Railway deployment"

# Pousser
git remote add origin VOTRE_REPO_URL
git push -u origin main
```