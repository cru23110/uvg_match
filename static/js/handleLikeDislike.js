function handleLikeDislike(action) {
    fetch('/handle_like_dislike', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action: action }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (data.redirect_url) {
                window.location.href = data.redirect_url;
            } else {
                location.reload();
            }
        } else {
            alert('Error al procesar la acción.');
        }
    });
}
