const textarea = document.querySelector('textarea');

textarea.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = this.scrollHeight + 'px';
});

async function createPost() {
    let response = await fetch('/api/v1/post/create/', {
        method: 'POST',
        redirect: "follow",
        mode: "no-cors",
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

    console.log(result);

    if (status === 200) {
        location.href = '/type/' + result['key'];
    } else {

    }
}
