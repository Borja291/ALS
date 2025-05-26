// Script para actualizar dinámicamente el modal de eliminar
const confirmDeleteModal = document.getElementById('confirmDeleteModal');
if (confirmDeleteModal) {
    confirmDeleteModal.addEventListener('show.bs.modal', event => {
        const button = event.relatedTarget;  // Botón que abrió el modal
        const title = button.getAttribute('data-title');  // Título del ítem a eliminar
        const deleteUrl = button.getAttribute('data-delete-url');  // URL donde enviar la eliminación

        document.getElementById('itemTitle').textContent = title;  // Muestra el título en el modal
        document.getElementById('deleteForm').action = deleteUrl;  // Asigna el destino del formulario
    });
}


// Para eliminar películas (confirmDeleteMovieModal)
const deleteMovieModal = document.getElementById('confirmDeleteMovieModal');
if (deleteMovieModal) {
    deleteMovieModal.addEventListener('show.bs.modal', event => {
        const button = event.relatedTarget;
        const title = button.getAttribute('data-movie-title');  // Título de la película
        const deleteUrl = button.getAttribute('data-delete-url');

        document.getElementById('movieTitle').textContent = `"${title}"`;  // Muestra el título entre comillas
        document.getElementById('confirmDeleteForm').action = deleteUrl;
    });
}


// Script para el modal de antes de añadir una película preguntar si todo está correcto
let confirmed = false;

function handleFormSubmit(event) {
    if (confirmed) return true;  // Si ya fue confirmado, continúa

    const form = event.target;
    if (!form.checkValidity()) {  // Si el formulario no es válido
        form.reportValidity();     // Muestra los errores
        return false;
    }

    event.preventDefault();  // Detiene el envío automático del formulario

    const confirmModalEl = document.getElementById('confirmModal');
    if (confirmModalEl) {
        const modal = new bootstrap.Modal(confirmModalEl);  // Crea el modal de confirmación
        modal.show();  // Lo muestra
    }

    return false;
}

function submitAfterConfirmation() {
    confirmed = true;  // Marca como confirmado
    document.getElementById('addMovieForm').submit();  // Envía el formulario
}


// Script para hacer que alerts desaparezcan solos

document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');  // Oculta visualmente (efecto fade de Bootstrap)
            alert.classList.add('fade');
            setTimeout(() => {
                alert.remove();  // Elimina del DOM tras el efecto
            }, 500);
        }, 3000);  // Espera 3 segundos antes de desaparecer
    });
});



// Mostrar/Ocultar reseñas
function toggleReviews(id) {
    const box = document.getElementById("reviews-" + id);  // Caja de reseñas
    const btn = document.getElementById("btn-" + id);      // Botón asociado

    if (box.style.display === "none" || box.style.display === "") {
        box.style.display = "block";
        btn.innerHTML = "🙈 Ocultar reseñas";
    } else {
        box.style.display = "none";
        btn.innerHTML = "👁 Ver reseñas";
    }
}


// Filtro de búsqueda en vivo
document.getElementById('searchInput').addEventListener('keyup', function () {
    const searchValue = this.value.toLowerCase();  // Valor de búsqueda en minúsculas
    const movieCards = document.querySelectorAll('.movie-card');  // Todas las tarjetas

    movieCards.forEach(card => {
        const title = card.getAttribute('data-title');  // Título en el atributo personalizado
        if (title.includes(searchValue)) {
            card.style.display = '';  // Mostrar si coincide
        } else {
            card.style.display = 'none';  // Ocultar si no
        }
    });
});
