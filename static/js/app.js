const html = document.getElementById('htmlpage');
const checkbox = document.getElementById('checkbox');
checkbox.addEventListener('change',() => {
    if (checkbox.checked) {
        html.setAttribute('data-bs-theme','light');
    } else {
        html.setAttribute('data-bs-theme', 'dark');
    }
});