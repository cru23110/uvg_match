document.addEventListener('DOMContentLoaded', function() {
    // Capturar el evento de clic en el botón "Pro"
    document.querySelector('.pro-control').addEventListener('click', function(event) {
        event.preventDefault(); // Evita que el enlace funcione por defecto

        // Realizar la animación antes de redireccionar a la nueva página
        animateTransition(function() {
            // Una vez finalizada la animación, redireccionar a la nueva página
            window.location.href = '/pro_version'; // Ir a pagina destino
        });
    });

    // Función para animar la transición entre páginas
    function animateTransition(callback) {
        var logo = document.querySelector('.logo-link img');
        var proLogo = document.createElement('img');
        proLogo.src = '../static/img/uvg_match_PRO.svg'; // Archivo del logo
        proLogo.alt = 'PRO Logo';
        proLogo.style.position = 'fixed';
        proLogo.style.top = '50%';
        proLogo.style.left = '50%';
        proLogo.style.transform = 'translate(-50%, -50%) scale(5)';
        proLogo.style.transition = 'transform 1s ease-in-out';
        
        document.body.appendChild(proLogo);

        setTimeout(function() {
            logo.style.opacity = '0';
            proLogo.style.transform = 'translate(-50%, -50%) scale(1)';
        }, 1000); // Esperar 1 segundo antes de iniciar la animación

        setTimeout(function() {
            proLogo.style.opacity = '0';
            callback(); // Llamar al callback después de que termine la animación
        }, 2000); // Esperar 2 segundos antes de ocultar el logo de PRO
    }
});
