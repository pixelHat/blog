document.addEventListener('DOMContentLoaded', () => {
});

const createContainer = (id, html) => {
    const element = document.createElement('div');
    element.className = "columns is-centered";
    element.id = `form-${id}`;
    element.innerHTML = html;
    return element;
}

const updateSubmit = () => {
    const form = document.querySelector("#form-reply");

    form.onsubmit = () => {
        const comment_id = form.comment_id.value;
        const text = form.text.value;
        const url = `/manager/comments/reply?comment_id=${comment_id}&text=${text}`;
        const request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.onload = () => {
            const data = JSON.parse(request.responseText);
            if (data.ok) {
                read(comment_id);
                replyClose(comment_id);
            }
        }
        request.send();
        return false;
    }
}

const replyComment = (id) => {
    const template = document.querySelector("#reply-comment-form-template");
    const values = {id_form: id}
    const output_mustache = Mustache.render(template.innerHTML, values);
    const comment = document.querySelector(`#card-${id}`);
    const element = createContainer(id, output_mustache);
    comment.parentNode.insertBefore(element, comment.nextSibling);
    updateSubmit();
}

const replyClose = (id) => {
    const form = document.querySelector(`#form-${id}`);
    form.style.display = 'none';
}
