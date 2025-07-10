// Placeholder front-end logic
fetch('/api/hello')
  .then(resp => resp.json())
  .then(data => {
    const div = document.getElementById('content');
    div.innerText = data.message;
  })
  .catch(err => console.error(err));
