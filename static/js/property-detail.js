let currentProperty = null;
let currentImageIndex = 0;

// Chargement des détails de la propriété
async function loadPropertyDetails() {
    const propertyId = window.location.pathname.split('/').pop();
    const content = document.getElementById('property-content');
    
    try {
        currentProperty = await API.get(`/api/properties/${propertyId}`);
        
        content.innerHTML = `
            <div class="property__gallery">
                <div class="gallery__main" onclick="openGallery(0)">
                    <img src="${currentProperty.images[0] || 'https://via.placeholder.com/800x500'}" alt="${currentProperty.titre}">
                </div>
                <div class="gallery__thumbnails">
                    ${currentProperty.images.slice(1, 4).map((img, index) => `
                        <div class="gallery__thumb" onclick="openGallery(${index + 1})">
                            <img src="${img}" alt="${currentProperty.titre}">
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="property__info">
                <div class="property__details">
                    <h1>${currentProperty.titre}</h1>
                    <div class="property__price-detail">${formatPrice(currentProperty.prix)}</div>
                    <div class="property__location-detail">
                        <i class="fas fa-map-marker-alt"></i>
                        ${currentProperty.localisation}
                    </div>
                    
                    <div class="property__features-detail">
                        <div class="feature__item">
                            <i class="fas fa-bed feature__icon"></i>
                            <div>
                                <strong>${currentProperty.chambres}</strong><br>
                                Chambres
                            </div>
                        </div>
                        <div class="feature__item">
                            <i class="fas fa-bath feature__icon"></i>
                            <div>
                                <strong>${currentProperty.salles_bain}</strong><br>
                                Salles de bain
                            </div>
                        </div>
                        ${currentProperty.surface ? `
                            <div class="feature__item">
                                <i class="fas fa-ruler-combined feature__icon"></i>
                                <div>
                                    <strong>${currentProperty.surface} m²</strong><br>
                                    Surface
                                </div>
                            </div>
                        ` : ''}
                        <div class="feature__item">
                            <i class="fas fa-home feature__icon"></i>
                            <div>
                                <strong>${currentProperty.type_propriete}</strong><br>
                                Type
                            </div>
                        </div>
                    </div>
                    
                    <div class="property__description">
                        <h3>Description</h3>
                        <p>${currentProperty.description}</p>
                    </div>
                </div>
                
                <div class="property__sidebar">
                    <h3>Intéressé par cette propriété ?</h3>
                    <button class="contact__btn" onclick="openReservationModal()">
                        <i class="fas fa-calendar-alt"></i>
                        Demander une visite
                    </button>
                    <button class="contact__btn" onclick="openReservationModal('Ferme')">
                        <i class="fas fa-handshake"></i>
                        Faire une offre
                    </button>
                    
                    <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e9ecef;">
                        <h4>Contactez-nous</h4>
                        <p><i class="fas fa-phone"></i> +1 (819) 123-4567</p>
                        <p><i class="fas fa-envelope"></i> contact@rkimmo.ca</p>
                    </div>
                </div>
            </div>
        `;
        
        // Mettre à jour le titre de la page
        document.title = `${currentProperty.titre} - RK IMMO`;
        
    } catch (error) {
        console.error('Erreur lors du chargement de la propriété:', error);
        content.innerHTML = `
            <div style="text-align: center; padding: 3rem;">
                <i class="fas fa-exclamation-triangle" style="font-size: 3rem; color: #e74c3c; margin-bottom: 1rem;"></i>
                <h2>Propriété non trouvée</h2>
                <p>Cette propriété n'existe pas ou a été supprimée.</p>
                <button onclick="window.location.href='/proprietes'" class="contact__btn">
                    Voir toutes les propriétés
                </button>
            </div>
        `;
    }
}

// Ouverture de la galerie
function openGallery(imageIndex) {
    if (!currentProperty || !currentProperty.images.length) return;
    
    currentImageIndex = imageIndex;
    const modal = document.getElementById('gallery-modal');
    const image = document.getElementById('gallery-image');
    const thumbnails = document.getElementById('gallery-thumbnails');
    
    image.src = currentProperty.images[currentImageIndex];
    
    // Générer les vignettes
    thumbnails.innerHTML = currentProperty.images.map((img, index) => `
        <img src="${img}" alt="Vignette ${index + 1}" 
             class="gallery__thumbnail ${index === currentImageIndex ? 'active' : ''}"
             onclick="changeGalleryImage(${index})">
    `).join('');
    
    modal.style.display = 'block';
}

// Changement d'image dans la galerie
function changeGalleryImage(index) {
    currentImageIndex = index;
    document.getElementById('gallery-image').src = currentProperty.images[index];
    
    // Mettre à jour les vignettes actives
    document.querySelectorAll('.gallery__thumbnail').forEach((thumb, i) => {
        thumb.classList.toggle('active', i === index);
    });
}

// Navigation dans la galerie
document.getElementById('gallery-prev').addEventListener('click', () => {
    if (currentProperty && currentProperty.images.length > 0) {
        currentImageIndex = (currentImageIndex - 1 + currentProperty.images.length) % currentProperty.images.length;
        changeGalleryImage(currentImageIndex);
    }
});

document.getElementById('gallery-next').addEventListener('click', () => {
    if (currentProperty && currentProperty.images.length > 0) {
        currentImageIndex = (currentImageIndex + 1) % currentProperty.images.length;
        changeGalleryImage(currentImageIndex);
    }
});

// Ouverture du modal de réservation
function openReservationModal(type = 'Visite') {
    const modal = document.getElementById('reservation-modal');
    const requestType = document.getElementById('request-type');
    const propertyId = document.getElementById('property-id');
    
    requestType.value = type;
    propertyId.value = currentProperty.id;
    modal.style.display = 'block';
}

// Gestion du formulaire de réservation
document.getElementById('reservation-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        propriete_id: parseInt(document.getElementById('property-id').value),
        nom_client: document.getElementById('client-name').value,
        email: document.getElementById('client-email').value,
        telephone: document.getElementById('client-phone').value,
        type_demande: document.getElementById('request-type').value,
        message: document.getElementById('client-message').value
    };
    
    const submitBtn = e.target.querySelector('.form__btn');
    const originalText = submitBtn.innerHTML;
    
    try {
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Envoi en cours...';
        submitBtn.disabled = true;
        
        const response = await API.post('/api/reservation', formData);
        
        if (response.success) {
            showNotification('Votre demande a été envoyée avec succès !', 'success');
            document.getElementById('reservation-modal').style.display = 'none';
            document.getElementById('reservation-form').reset();
        } else {
            throw new Error(response.message || 'Erreur lors de l\'envoi');
        }
        
    } catch (error) {
        console.error('Erreur lors de l\'envoi de la réservation:', error);
        showNotification('Erreur lors de l\'envoi de la demande. Veuillez réessayer.', 'error');
    } finally {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

// Fermeture des modals
document.querySelectorAll('.modal__close').forEach(closeBtn => {
    closeBtn.addEventListener('click', (e) => {
        e.target.closest('.modal').style.display = 'none';
    });
});

// Fermeture des modals en cliquant à l'extérieur
document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
});

// Navigation au clavier dans la galerie
document.addEventListener('keydown', (e) => {
    const galleryModal = document.getElementById('gallery-modal');
    if (galleryModal.style.display === 'block') {
        if (e.key === 'ArrowLeft') {
            document.getElementById('gallery-prev').click();
        } else if (e.key === 'ArrowRight') {
            document.getElementById('gallery-next').click();
        } else if (e.key === 'Escape') {
            galleryModal.style.display = 'none';
        }
    }
});

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    loadPropertyDetails();
});