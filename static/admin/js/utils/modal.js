document.addEventListener("DOMContentLoaded", function () {
    const modalButtons = document.querySelectorAll(".trigger");
    const modals = document.querySelectorAll(".modal");
    const modalContents = document.querySelectorAll(".modal-content");
    const closeButton = document.querySelectorAll(".close-button, .close-sign");

    function toggleModal(event) {
        const modalId = event.target.getAttribute("data-modal-id");
        const modal = document.getElementById(modalId);
        modal.classList.toggle("show-modal");
    }

    function closeModal(event) {
        if (event.target === event.currentTarget) {
            event.target.classList.remove("show-modal");
        }
    }

    modalButtons.forEach((button) => {
        button.addEventListener("click", toggleModal);
    });

    closeButton.forEach((button) => {
        button.addEventListener("click", function (event) {
            const modal = event.target.closest(".modal");
            modal.classList.remove("show-modal");
        });
    });

    modals.forEach((modal) => {
        modal.addEventListener("click", closeModal);
    });

    modalContents.forEach((content) => {
        content.addEventListener("click", (event) => {
            event.stopPropagation();
        });
    });
});