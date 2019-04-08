document.addEventListener('DOMContentLoaded', () => {
    new Tabs();
});

class Tabs {
    constructor() {
        const tabs_list = document.querySelectorAll('.tabs ul');
        this.start(tabs_list);
        this.create_clicks(tabs_list);
    }

    start(tabs_list) {
        for (const tabs of tabs_list) {
            const id_container_content = tabs.dataset.container;
            for (const li of tabs.children)
                if (!li.className.includes("is-active"))
                    this.hidden_content(li, id_container_content);
        }
    }

    create_clicks(tabs_list) {
        for (const tabs of tabs_list) {
            const id_container_content = tabs.dataset.container;
            const li_list = tabs.children;
            for (const li of li_list) {
                const link = li.children[0];
                link.onclick = (event) => {
                    this.add_click(event, li_list, id_container_content);
                };
            }
        }
    }

    add_click(event, li_list, id_container_content) {
        for (const li of li_list) {
            this.hidden_content(li, id_container_content);
        }
        const id_content = event.target.dataset.content;
        const content = document.querySelector(`#${id_container_content} #${id_content}`);
        content.style.display = 'block';
        event.target.parentNode.classList.add('is-active');
    }

    hidden_content(li, id_container_content) {
        const link = li.children[0];
        const id_content = link.dataset.content;
        li.classList.remove("is-active");
        const content = document.querySelector(`#${id_container_content} #${id_content}`);
        content.style.display = 'none';
    }
}
