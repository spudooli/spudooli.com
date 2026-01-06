document.addEventListener('DOMContentLoaded', function () {
    // --- Comment Form Logic ---

    // Function to toggle display (equivalent to 'flip')
    function toggleDisplay(elementId) {
        const el = document.getElementById(elementId);
        if (el) {
            const currentDisplay = window.getComputedStyle(el).display;
            el.style.display = (currentDisplay === 'none') ? 'block' : 'none';
        }
    }

    // Function to scroll to comments (equivalent to 'gotocomments')
    function scrollToComments() {
        window.location.hash = 'addcomment';
    }

    // Initialize comment form state (hide it initially)
    const commentForm = document.getElementById('add-comment');
    if (commentForm) {
        // We want it hidden initially. The original logic called flip('add-comment') 
        // which toggled it from default (block) to none.
        // It's better to verify if we should hide it or if CSS handles it, 
        // but for parity with original JS execution:
        commentForm.style.display = 'none';
    }

    // Attach listener to "Add your own comment" link
    const addCommentLink = document.getElementById('link-add-comment');
    if (addCommentLink) {
        addCommentLink.addEventListener('click', function (e) {
            e.preventDefault();
            toggleDisplay('add-comment');
            scrollToComments();
        });
    }


    // --- Modal Logic ---
    const modal = document.getElementById('modal');
    const modalImage = document.getElementById('modal-image');

    // Open Modal
    const openModalBtn = document.getElementById('btn-open-modal');
    if (openModalBtn && modal && modalImage) {
        openModalBtn.addEventListener('click', function () {
            const imageSrc = openModalBtn.getAttribute('data-image-src');
            if (imageSrc) {
                modalImage.src = imageSrc;
                modal.style.display = 'block';
            }
        });
    }

    // Close Modal (X button)
    const closeModalBtn = document.getElementById('btn-close-modal');
    if (closeModalBtn && modal) {
        closeModalBtn.addEventListener('click', function () {
            modal.style.display = 'none';
        });
    }

    // Close Modal (Click outside)
    if (modal) {
        window.addEventListener('click', function (event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
});
