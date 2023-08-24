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
    } else {

    }
}

//const fileInput = document.querySelector('input[type="file"]');
//
//fileInput.addEventListener('change', (event) => {
//    const file = event.target.files[0];
//    if (file) {
//        async function uploadImage() {
//        const formData = new FormData();
//        formData.append('image', file);
//
//        try {
//            const response = fetch('/api/v1/image/upload', {
//                method: 'POST',
//                body: formData
//            });
//            if (!response.ok) {
//                throw new Error(`Error! status: ${response.status}`);
//            }
//
//            const result = response.json();
//            return result;
//        } catch (err) {
//            console.log(err);
//        }
//        const status = response.status;
//        console.log(response.json());
//    }
//        await createPost();
//    }
//});