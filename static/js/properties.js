let currentProperties = [];

// Chargement des propriétés
async function loadProperties(filters = {}) {
    const loading = document.getElementById('loading');
    const grid = document.getElementById('properties-grid');
    
    loading.style.display = 'block';
    
    try {
        // Construire l'URL avec les filtres
        const params = new URLSearchParams();
        Object.keys(filters).forEach(key => {
            if (filters[key]) params.append(key, filters[key]);
        });
        
        const properties = await API.get(`/api/properties?${params.toString()}`);
        currentProperties = properties;
        
        loading.style.display = 'none';
        
        if (properties.length === 0) {
            grid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
                    <i class="fas fa-home" style="font-size: 3rem; color: #bdc3c7; margin-bottom: 1rem;"></i>
                    <h3>Aucune propriété trouvée</h3>
                    <p>Essayez de modifier vos critères de recherche.</p>
                </div>
            `;
            return;
        }
        
        grid.innerHTML = properties.map(property => createPropertyCard(property)).join('');
        
        // Réactiver l'observer pour les nouvelles cartes
        const newCards = grid.querySelectorAll('.property__card');
        newCards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
            observer.observe(card);
        });
        
    } catch (error) {
        console.error('Erreur lors du chargement des propriétés:', error);
        loading.style.display = 'none';
        grid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 3rem;">
                <i class="fas fa-exclamation-triangle" style="font-size: 3rem; color: #e74c3c; margin-bottom: 1rem;"></i>
                <h3>Erreur de chargement</h3>
                <p>Impossible de charger les propriétés. Veuillez réessayer.</p>
            </div>
        `;
    }
}

// Gestion des filtres
function applyFilters() {
    const filters = {
        localisation: document.getElementById('filter-location').value,
        type: document.getElementById('filter-type').value,
        prix_min: document.getElementById('filter-price-min').value,
        prix_max: document.getElementById('filter-price-max').value
    };
    
    // Supprimer les filtres vides
    Object.keys(filters).forEach(key => {
        if (!filters[key]) delete filters[key];
    });
    
    loadProperties(filters);
}

// Event listeners
document.getElementById('apply-filters').addEventListener('click', applyFilters);

// Filtrage en temps réel sur les champs de texte
document.getElementById('filter-location').addEventListener('input', debounce(applyFilters, 500));
document.getElementById('filter-type').addEventListener('change', applyFilters);
document.getElementById('filter-price-min').addEventListener('input', debounce(applyFilters, 500));
document.getElementById('filter-price-max').addEventListener('input', debounce(applyFilters, 500));

// Fonction debounce pour éviter trop d'appels API
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initialisation avec les paramètres URL
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const initialFilters = {};
    
    // Remplir les champs avec les paramètres URL
    if (urlParams.get('localisation')) {
        document.getElementById('filter-location').value = urlParams.get('localisation');
        initialFilters.localisation = urlParams.get('localisation');
    }
    if (urlParams.get('type')) {
        document.getElementById('filter-type').value = urlParams.get('type');
        initialFilters.type = urlParams.get('type');
    }
    if (urlParams.get('prix_max')) {
        document.getElementById('filter-price-max').value = urlParams.get('prix_max');
        initialFilters.prix_max = urlParams.get('prix_max');
    }
    
    loadProperties(initialFilters);
});