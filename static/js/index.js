const textarea = document.querySelector('textarea');

textarea.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = this.scrollHeight + 'px';
});

async function createPost() {
    let response = await fetch('/api/v1/post/create/', {
        method: 'POST',
	    mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
        host: 'pixeltype.egoryolkin.ru',
        Origin: 'https://pixeltype.egoryolkin.ru',
        body: JSON.stringify({
            title: document.getElementById('titleInput').value,
            text: document.getElementById('textInput').value,
            author: document.getElementById('authorInput').value
        })
    });

    let status = response.status;
    let result = await response.json();

    console.log(result);

    if (status === 200) {
        location.href = '/type/' + result['key'];
    } else {

    }
}
