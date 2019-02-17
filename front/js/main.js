document.addEventListener('DOMContentLoaded', () => {
    const navButton = document.querySelector('#menu-button');
    navButton.addEventListener('click', () => {
        const id = navButton.dataset.target;
        const menuItems = document.querySelector(`#${id}`);
        navButton.classList.toggle('is-active');
        menuItems.classList.toggle('is-active');
    });
});
