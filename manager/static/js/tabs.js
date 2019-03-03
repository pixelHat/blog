document.addEventListener('DOMContentLoaded', () => {
    const tab_waiting_comments = document.querySelector("#waiting");
    let id = tab_waiting_comments.dataset.id;
    const container_waiting_comments = document.querySelector(`#${id}`);

    const tab_new_comments = document.querySelector("#new");
    id = tab_new_comments.dataset.id;
    const container_new_comments = document.querySelector(`#${id}`);

    tab_waiting_comments.addEventListener('click', () => {
        tab_waiting_comments.classList.toggle('is-active');
        tab_new_comments.classList.toggle('is-active');
        container_waiting_comments.style.display = 'block';
        container_new_comments.style.display = 'none';
    });

    tab_new_comments.addEventListener('click', () => {
        tab_waiting_comments.classList.toggle('is-active');
        tab_new_comments.classList.toggle('is-active');
        container_waiting_comments.style.display = 'none';
        container_new_comments.style.display = 'block';
    });
})
