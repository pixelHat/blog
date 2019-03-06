class CommmentsContainer {
    constructor(id) {
        this.link = document.querySelector(`#${id}`);
        const id_container = this.link.dataset.id;
        this.container_comments = document.querySelector(`#${id_container}`);
    }

    click = () => {
        this.link.classList.toggle('is-active');
        this.toggleStyleDisplay();
    }

    toggleStyleDisplay = () => {
        const style = getComputedStyle(this.container_comments);
        if (style.display === "block") {
            this.container_comments.style.display = "none";
        }
        else
            this.container_comments.style.display = "block";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const id_waiting_comments = 'waiting';
    const id_new_comments = 'new';
    const tabs = [document.querySelector(`#${id_waiting_comments}`),
                  document.querySelector(`#${id_new_comments}`)
    ]
    const waiting_comments = new CommmentsContainer(id_waiting_comments);
    const new_comments = new CommmentsContainer(id_new_comments);
    tabs.forEach((tab) => {
        tab.addEventListener('click', () => {
            waiting_comments.click();
            new_comments.click();
        });
    });
})
