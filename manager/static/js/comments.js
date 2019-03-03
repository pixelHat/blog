document.addEventListener('DOMContentLoaded', () => {
});

createContainer = (id, html) => {
    const element = document.createElement('div');
    element.className = "columns is-centered";
    element.id = `form-${id}`;
    element.innerHTML = html;
    return element;
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
                read(comment_id);
                replyClose(comment_id);
            }
        }
        request.send();
        return false;
    }
}

replyComment = (id) => {
    const template = document.querySelector("#reply-comment-form-template");
    const values = {id_form: id}
    const output_mustache = Mustache.render(template.innerHTML, values);
    const comment = document.querySelector(`#card-${id}`);
    const element = createContainer(id, output_mustache);
    comment.parentNode.insertBefore(element, comment.nextSibling);
    updateSubmit();
}

replyClose = (id) => {
    const form = document.querySelector(`#form-${id}`);
    form.style.display = 'none';
}


/**
 * remove the html of the comment.
**/
removeCard = (id) => {
    const comment = document.querySelector(`#card-${id}`);
    comment.style.display = 'none';
}

/**
 * send one request to server.
**/
request = (id, url) => {
    const request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = () => {
        const data = JSON.parse(request.responseText)
        if (data.ok)
            removeCard(id);
    }
    request.send();
}

/**
 * set the comment with readed.
**/
read = (id) => {
    const url = `/manager/comments/read?id=${id}`
    request(id, url);
}

/**
 * delete a comment from database.
**/
deleteComment = (id) => {
    const url = `/manager/comments/delete?id=${id}`;
    request(id, url);
}

/**
 * set the comment for read later.
**/
addWaitListComment = (id) => {
    const url = `/manager/comments/add/waitList?id=${id}`;
    request(id, url);
}
