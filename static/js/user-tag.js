$(document).ready(function(){
    $('[data-toggle="popover"]').popover({
        placement: 'bottom', // Posición de la ventana emergente (opcional)
        trigger: 'hover click', // Eventos para mostrar la ventana emergente
        html: true // Permitir contenido HTML en la ventana emergente.
    });
});