// Вы можете определить базовый URL-адрес в зависимости от среды
let baseUrl;
if (window.location.hostname === 'localhost' || 
    window.location.hostname === '127.0.0.1') {
    baseUrl = 'http://localhost:8000'; // Замените на ваш локальный URL
} else {
    baseUrl = 'https://pixeltype.egoryolkin.ru'; // Замените на ваш хостинг URL
}


function formatDate(dateStr) {
    var date = new Date(dateStr);
    var currentYear = new Date().getFullYear();
    var currentTime = new Date().getTime();
    var diffTime = currentTime - date.getTime();
    var diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (date.getFullYear() == currentYear) {
        return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' }) + ' (' + diffDays + ' дней назад)';
    } else {
        return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' }) + ' (' + diffDays + ' дней назад)';
    }
}


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

    let author = document.getElementById('authorInput').value;
        
    if (author.length === 0) {
        author = undefined;
    } 

    let response = await fetch(`${baseUrl}/api/v1/post/create`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            title: document.getElementById('titleInput').value,
            text: document.getElementById('textInput').value,
            author: author
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
        const response = await fetch(`${baseUrl}/api/v1/post/image/upload`, {
            method: 'POST',
            body: formData
        });
        return await response.json();
    } catch (err) {
    }
}


async function createComment(post_key) {
    localStorage.setItem('author', document.getElementById('commentAuthorInput').value);

    let author = document.getElementById('commentAuthorInput').value;
        
    if (author.length === 0) {
        author = undefined;
    } 

    let response = await fetch(`${baseUrl}/api/v1/comments/create`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            text: document.getElementById('commentTextInput').value,
            author: author, 
            post_key: post_key
        })
    });

    let status = response.status;

    if (status === 201) {
        document.getElementById('commentAuthorInput').value = "";
        document.getElementById('commentTextInput').value = "";

        getPostComments(post_key);
    } else {

    }
}


async function getPostComments(post_key) {
    let response = await fetch(`${baseUrl}/api/v1/comments/get/${post_key}/`, {
        method: 'GET'
    });
    let status = response.status;
    let result = await response.json();

    if (status === 200) {
        if (result.length > 0) {
            let content = '';
            for (let item in result) {
                let elem = result[item];

                let html = `
                <div class="card mb-4">
                    <div class="card-body">
                        <br>
                        <p>${elem.text}</p>
                        <br>
                        <div class="d-flex justify-content-between">
                            <div>
                                <mark class="roman" style="border-radius: 5px; padding: 7px 7px 7px 7px">
                                ${elem.author}
                                </mark>
                            </div>
                            <div class="d-flex flex-row align-items-center">
                                <p class="small text-muted mb-0">${formatDate(elem.created)}</p>
                            </div>
                        </div>
                    </div>
                </div>
                `
                content += html;
            }
            let block = document.getElementById('comments');
            block.innerHTML = content;

            document.getElementById("commentsCount").innerHTML = result.length;
        }
    }
}