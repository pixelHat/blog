removeCard = (id) => {
    const comment = document.querySelector(`#card-${id}`);
    comment.style.display = 'none';
}

createReplyFormContainer = (id, html) => {
    const element = document.createElement('div');
    element.className = "columns is-centered";
    element.id = `form-${id}`;
    element.innerHTML = html;
    return element;
}

createReplyForm = (id) => {
    const template = document.querySelector("#reply-comment-form-template");
    const values = {id_form: id}
    const output_mustache = Mustache.render(template.innerHTML, values);
    return createReplyFormContainer(id, output_mustache);
}

updateSubmit = () => {
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
                readComment(comment_id);
                replyFormClose(comment_id);
            }
        }
        request.send();
        return false;
    }
}

replyComment = (id) => {
    const replyForm = createReplyForm(id);
    const comment = document.querySelector(`#card-${id}`);
    comment.parentNode.insertBefore(replyForm, comment.nextSibling);
    updateSubmit();
}

replyFormClose = (id) => {
    const form = document.querySelector(`#form-${id}`);
    form.style.display = 'none';
}

request = (id, url) => {
    const request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = () => {
        const data = JSON.parse(request.responseText)
        if (data.ok)
            this.removeCard(id);
    }
    request.send();
}

readComment = (id) => {
    const url = `/manager/comments/read?id=${id}`
    request(id, url);
}

deleteComment = (id) => {
    const url = `/manager/comments/delete?id=${id}`;
    request(id, url);
}

addWaitListComment = (id) => {
    const url = `/manager/comments/add/waitList?id=${id}`;
    request(id, url);
}
