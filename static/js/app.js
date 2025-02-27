// Initialize tooltips
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

// Alert dismiss functionality
document.querySelectorAll('.alert-dismiss').forEach(button => {
    button.addEventListener('click', (e) => {
        e.target.closest('.alert-card').remove();
    });
});

// Search form validation
const searchForm = document.querySelector('.search-form');
if (searchForm) {
    searchForm.addEventListener('submit', (e) => {
        const input = e.target.querySelector('input');
        if (input.value.trim() === '') {
            e.preventDefault();
            input.classList.add('is-invalid');
            setTimeout(() => input.classList.remove('is-invalid'), 1000);
        }
    });
}

// Favorite item hover effects
document.querySelectorAll('.favorite-item').forEach(item => {
    item.addEventListener('mouseenter', () => {
        item.style.transform = 'translateX(5px)';
    });
    item.addEventListener('mouseleave', () => {
        item.style.transform = 'translateX(0)';
    });
});