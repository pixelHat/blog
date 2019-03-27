class CommmentsContainer {
    constructor(tab_link, id_container) {
        this.link = tab_link;
        this.container_comments = document.querySelector(`#${id_container}`);
    }

    show = () => {
        this.link.classList.add('is-active');
        this.container_comments.style.display = "block";
    }

    hidden = () => {
        this.link.classList.remove("is-active");
        this.container_comments.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const tabs_links = document.querySelectorAll(".is-tab-link");
    const containers = getContainers(tabs_links);
    const tabs_links_length = tabs_links.length;
    const containers_length = containers.length;
    for (let i = 0; i < tabs_links_length; i++) {
        tabs_links[i].addEventListener('click', (event) => {
            containers[i].show();
            const hiddens_index = generateSeries(containers_length);
            hiddens_index.splice(i, 1);
            for (const j of hiddens_index)
                containers[j].hidden();
        });
    }
})

getContainers = (tabs_links) => {
    const containers = []
    for(let tab_link of tabs_links) {
        const id = tab_link.dataset.id;
        const container = new CommmentsContainer(tab_link, id);
        containers.push(container);
    }
    return containers;
}

generateSeries = (max) => {
    const series = Array.apply(0, Array(max)).map((_, idx) => idx);
    return series;
}
