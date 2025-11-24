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

// Carousel functionality
let currentSlide = 0;
const slides = document.querySelectorAll('.carousel__slide');
const dots = document.querySelectorAll('.dot');
const totalSlides = slides.length;

function updateCarousel() {
    slides.forEach((slide, index) => {
        slide.classList.toggle('active', index === currentSlide);
        // Mettre à jour le background
        if (index === currentSlide) {
            slide.style.backgroundImage = `url(${slide.dataset.bg})`;
        }
    });
    
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentSlide);
    });
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    updateCarousel();
}

function prevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    updateCarousel();
}

function goToSlide(index) {
    currentSlide = index;
    updateCarousel();
}

// Event listeners pour le carousel
if (document.querySelector('.carousel__next')) {
    document.querySelector('.carousel__next').addEventListener('click', nextSlide);
    document.querySelector('.carousel__prev').addEventListener('click', prevSlide);
    
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => goToSlide(index));
    });
    
    // Auto-play du carousel
    setInterval(nextSlide, 5000);
    
    // Initialiser le carousel
    updateCarousel();
}

// Navigation au clavier pour le carousel
document.addEventListener('keydown', (e) => {
    if (document.querySelector('.hero-carousel')) {
        if (e.key === 'ArrowLeft') {
            prevSlide();
        } else if (e.key === 'ArrowRight') {
            nextSlide();
        }
    }
});

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    loadFeaturedProperties();
});