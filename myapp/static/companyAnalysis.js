function searchCompany() {
    var searchQuery = document.getElementById("searchQuery").value;

    fetch('/api/company-info/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ searchQuery: searchQuery })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("companyInfo").style.display = 'block';
        document.getElementById("companyName").textContent = data.name;
        document.getElementById("companyDescription").textContent = data.description;
    })
    .catch(error => console.error('Error:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
