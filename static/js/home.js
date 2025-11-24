// Chargement des propriétés en vedette
async function loadFeaturedProperties() {
    try {
        const properties = await API.get('/api/properties');
        const featuredContainer = document.getElementById('featured-properties');
        
        if (properties.length === 0) {
            featuredContainer.innerHTML = '<p>Aucune propriété disponible pour le moment.</p>';
            return;
        }
        
        // Prendre les 3 premières propriétés comme vedettes
        const featuredProperties = properties.slice(0, 3);
        featuredContainer.innerHTML = featuredProperties.map(property => createPropertyCard(property)).join('');
        
        // Réactiver l'observer pour les nouvelles cartes
        const newCards = featuredContainer.querySelectorAll('.property__card');
        newCards.forEach(card => observer.observe(card));
        
    } catch (error) {
        console.error('Erreur lors du chargement des propriétés:', error);
        document.getElementById('featured-properties').innerHTML = 
            '<p>Erreur lors du chargement des propriétés.</p>';
    }
}

// Gestion du formulaire de recherche
document.getElementById('search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const location = document.getElementById('search-location').value;
    const type = document.getElementById('search-type').value;
    const price = document.getElementById('search-price').value;
    
    // Construire l'URL avec les paramètres de recherche
    const params = new URLSearchParams();
    if (location) params.append('localisation', location);
    if (type) params.append('type', type);
    if (price) params.append('prix_max', price);
    
    // Rediriger vers la page des propriétés avec les filtres
    window.location.href = `/proprietes?${params.toString()}`;
});

// Parallax effect pour le hero
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroBackground = document.querySelector('.hero__bg');
    if (heroBackground) {
        heroBackground.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    loadFeaturedProperties();
});