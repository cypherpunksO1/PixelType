function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    alert("Copy!");
}

function addHashToStart(str) {
    if (str.charAt(0) !== "#") {
        str = "#" + str;
    }
    return str;
}

function copyTitleToClipboard(title) {
    copyToClipboard(window.location.href + addHashToStart(title.slice(1)));
}


async function createPost() {
    localStorage.setItem('author', document.getElementById('authorInput').value);

    let response = await fetch('/api/v1/post/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            title: document.getElementById('titleInput').value,
            text: document.getElementById('textInput').value,
            author: document.getElementById('authorInput').value
        })
    });

    let status = response.status;
    let result = await response.json();

    if (status === 200) {
        location.href = '/type/' + result['key'];

        localStorage.removeItem('text')
        localStorage.removeItem('title')
    } else {

    }
}

async function uploadImage(file) {
    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('/api/v1/image/upload', {
            method: 'POST',
            body: formData
        });
        return await response.json();
    } catch (err) {
    }
}

const fileInput = document.querySelector('input[type="file"]');
fileInput.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (file) {
        const result = await uploadImage(file);
        insertText('![](/' + result['path'] + ')')

        localStorage.setItem('text', document.getElementById('textInput').value);
        localStorage.setItem('title', document.getElementById('titleInput').value);
    }
});