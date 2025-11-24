// Navigation mobile
const navToggle = document.getElementById('nav-toggle');
const navMenu = document.getElementById('nav-menu');

if (navToggle) {
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('show');
    });
}

// Fermer le menu mobile lors du clic sur un lien
document.querySelectorAll('.nav__link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('show');
    });
});

// Header sticky avec effet
const header = document.getElementById('header');
let lastScrollY = window.scrollY;

window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        header.style.background = 'rgba(255, 255, 255, 0.98)';
        header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.15)';
    } else {
        header.style.background = 'rgba(255, 255, 255, 0.95)';
        header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    }
    lastScrollY = window.scrollY;
});

// Animation au scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observer tous les éléments avec animation
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.section__title, .property__card, .service__card');
    animatedElements.forEach(el => {
        observer.observe(el);
    });
});

// Utilitaires API
const API = {
    async get(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            throw error;
        }
    },

    async post(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            throw error;
        }
    }
};

// Formatage du prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-CA', {
        style: 'currency',
        currency: 'CAD',
        minimumFractionDigits: 0
    }).format(price);
}

// Création d'une carte de propriété
function createPropertyCard(property) {
    const mainImage = property.images && property.images.length > 0 ? property.images[0] : 'https://via.placeholder.com/400x250';
    
    return `
        <div class="property__card" style="animation-delay: ${Math.random() * 0.5}s">
            <div class="property__image">
                <img src="${mainImage}" alt="${property.titre}" loading="lazy">
                <div class="property__status">${property.statut}</div>
            </div>
            <div class="property__content">
                <div class="property__price">${formatPrice(property.prix)}</div>
                <h3 class="property__title">${property.titre}</h3>
                <div class="property__location">
                    <i class="fas fa-map-marker-alt"></i>
                    ${property.localisation}
                </div>
                <div class="property__features">
                    <div class="property__feature">
                        <i class="fas fa-bed"></i>
                        ${property.chambres} ch.
                    </div>
                    <div class="property__feature">
                        <i class="fas fa-bath"></i>
                        ${property.salles_bain} sdb.
                    </div>
                    ${property.surface ? `
                        <div class="property__feature">
                            <i class="fas fa-ruler-combined"></i>
                            ${property.surface} m²
                        </div>
                    ` : ''}
                </div>
                <button class="property__btn" onclick="window.location.href='/propriete/${property.id}'">
                    Voir les détails
                </button>
            </div>
        </div>
    `;
}

// Notification toast
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification--${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        ${message}
    `;
    
    // Styles pour la notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        background: type === 'success' ? '#27ae60' : '#e74c3c',
        color: 'white',
        padding: '1rem 1.5rem',
        borderRadius: '8px',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
        zIndex: '9999',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    document.body.appendChild(notification);
    
    // Animation d'entrée
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Suppression automatique
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 4000);
}