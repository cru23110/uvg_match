document.addEventListener('DOMContentLoaded', function() {
    // Capturar el evento de clic en el botón "Pro"
    document.querySelector('.pro-control').addEventListener('click', function(event) {
        event.preventDefault(); // Evita que el enlace funcione por defecto

        // Realizar la animación antes de redireccionar a la nueva página
        animateTransition(function() {
            // Una vez finalizada la animación, redireccionar a la nueva página
            window.location.href = '/pro_version'; // Ir a la página destino
        });
    });

    // Función para animar la transición entre páginas
    function animateTransition(callback) {
        var proLogo = document.createElement('img');
        var normalLogo = document.createElement('img');
        var overlay = document.createElement('div');
    
        // Configuración del overlay
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.backgroundColor = '#f0f0f0'; // Color de fondo
        overlay.style.zIndex = '999'; // Asegurar que esté por encima de otros elementos
        overlay.style.opacity = '0'; // Comenzar con opacidad cero
        overlay.style.transition = 'opacity 1s ease-in-out'; // Transición de opacidad
    
        // Configuración del logo normal
        normalLogo.src = '../static/img/uvg_match.svg'; // Ruta al logo normal
        normalLogo.alt = 'Normal Logo';
        normalLogo.style.position = 'fixed';
        normalLogo.style.top = '50%';
        normalLogo.style.left = '50%';
        normalLogo.style.transform = 'translate(-50%, -50%) scale(1)'; // Escala inicial
        normalLogo.style.opacity = '0'; // Comenzar con opacidad cero
        normalLogo.style.transition = 'opacity 1s ease-in-out'; // Transición de opacidad
        normalLogo.style.zIndex = '1000'; // Asegurar que esté por encima del overlay
    
        // Agregar el overlay al cuerpo del documento
        document.body.appendChild(overlay);
    
        // Agregar el logo normal al cuerpo del documento
        document.body.appendChild(normalLogo);
    
        // Mostrar el overlay y el logo normal juntos
        setTimeout(function() {
            overlay.style.opacity = '1'; // Mostrar el overlay
            normalLogo.style.opacity = '1'; // Mostrar el logo normal
        }, 100);
    
        // Esperar un poco antes de agregar el logo PRO al DOM
        setTimeout(function() {
            // Configuración del logo PRO
            proLogo.src = '../static/img/uvg_match_PRO.svg'; // Ruta al logo PRO
            proLogo.alt = 'PRO Logo';
            proLogo.style.position = 'fixed';
            proLogo.style.top = '50%';
            proLogo.style.left = '50%';
            proLogo.style.transform = 'translate(-50%, -50%) scale(5)'; // Escala inicial
            proLogo.style.opacity = '0'; // Comenzar con opacidad cero
            proLogo.style.transition = 'transform 1s ease-in-out, opacity 1s ease-in-out'; // Transición de escala y opacidad
            proLogo.style.zIndex = '1000'; // Asegurar que esté por encima del overlay
    
            // Agregar el logo PRO al cuerpo del documento
            document.body.appendChild(proLogo);
    
            // Mostrar el logo PRO y ocultar el logo normal
            setTimeout(function() {
                normalLogo.style.opacity = '0'; // Ocultar el logo normal
                proLogo.style.transform = 'translate(-50%, -50%) scale(1)';
                proLogo.style.opacity = '1'; // Mostrar el logo PRO
            }, 1000);
    
            // Ocultar el logo PRO, el logo normal y el overlay y llamar al callback después de la animación
            setTimeout(function() {
                proLogo.style.opacity = '0'; // Ocultar el logo de PRO
                overlay.style.opacity = '0'; // Ocultar el overlay
                callback(); // Llamar al callback después de la animación
            }, 2800);
        }, 100); // Esperar 0.1 segundos antes de agregar el logo PRO al DOM
    }
    
});
