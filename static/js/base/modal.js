function openModal(idModal) {
    const modalElement = document
        .getElementById(idModal);

    modalElement.classList.remove('hidden');
}

function closeModal(idModal) {
    const modalElement = document
        .getElementById(idModal);

    modalElement.classList.add('hidden');
}

Array.from(document.querySelectorAll('.btn-modal')).forEach(element => {
    element.addEventListener('click', () => {
        const idModal = element.getAttribute('modal');
        openModal(idModal);
    });
});

Array.from(document.querySelectorAll('.btn-close-modal')).forEach(element => {
    element.addEventListener('click', () => {
        const idModal = element.getAttribute('modal');
        closeModal(idModal);
    });
});