const textarea = document.querySelector('textarea');

textarea.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = this.scrollHeight + 'px';

  if (localStorage.getItem('draftText') && this.value.length > localStorage.getItem('draftText').length) {
      localStorage.setItem('draftTitle', document.getElementById('titleInput').value);
      localStorage.setItem('draftText', this.value);
      document.getElementById('loadDraftButton').style.display = 'none';
  } else {
    document.getElementById('loadDraftButton').style.display = 'block';
  }
});


//const fontSwitch = document.getElementById('fontSwitch');
//const headerElement = document.querySelector('header');
//
//fontSwitch.addEventListener('change', function() {
//    console.log(this.checked);
//    if (this.checked) {
//        bodyElement.style.fontFamily = 'joystix';
//    } else {
////    bodyElement.style.fontFamily = 'monospace';
//        headerElement.style.fontFamily = 'Helvetica';
//    }
//});


function loadDraft() {
    console.log(localStorage.getItem('draftText'));
    document.getElementById('titleInput').value = localStorage.getItem('draftTitle');
    document.getElementById('textInput').value = localStorage.getItem('draftText');
}


async function createPost() {
    let response = await fetch('/api/v1/post/create/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
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