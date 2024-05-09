// Función para actualizar la edad mínima
function actualizarEdadMinima(valor) {
    // Obtener el valor actual de la edad máxima
    var edadMaxima = parseInt(document.getElementById("edad_maxima").value);

    // Verificar si la edad mínima es mayor que la edad máxima
    if (parseInt(valor) > edadMaxima) {
        // Si la edad mínima es mayor que la edad máxima, ajustar la edad máxima
        document.getElementById("edad_maxima").value = valor;
        // Actualizar el valor mostrado para la edad máxima
        document.getElementById("valor_edad_maxima").innerHTML = valor;
    }

    // Actualizar el valor mostrado para la edad mínima
    document.getElementById("valor_edad_minima").innerHTML = valor;
}

// Función para actualizar la edad máxima
function actualizarEdadMaxima(valor) {
    // Obtener el valor actual de la edad mínima
    var edadMinima = parseInt(document.getElementById("edad_minima").value);

    // Verificar si la edad máxima es menor que la edad mínima
    if (parseInt(valor) < edadMinima) {
        // Si la edad máxima es menor que la edad mínima, ajustar la edad mínima
        document.getElementById("edad_minima").value = valor;
        // Actualizar el valor mostrado para la edad mínima
        document.getElementById("valor_edad_minima").innerHTML = valor;
    }

    // Actualizar el valor mostrado para la edad máxima
    document.getElementById("valor_edad_maxima").innerHTML = valor;
}

// Función para actualizar la distancia mínima
function actualizarDistanciaMinima(valor) {
    // Obtener el valor actual de la distancia máxima
    var distanciaMaxima = parseInt(document.getElementById("distancia_maxima").value);

    // Verificar si la distancia mínima es mayor que la distancia máxima
    if (parseInt(valor) > distanciaMaxima) {
        // Si la distancia mínima es mayor que la distancia máxima, ajustar la distancia máxima
        document.getElementById("distancia_maxima").value = valor;
        // Actualizar el valor mostrado para la distancia máxima
        document.getElementById("valor_distancia_maxima").innerHTML = valor + " km";
    }

    // Actualizar el valor mostrado para la distancia mínima
    document.getElementById("valor_distancia_minima").innerHTML = valor + " km";
}

// Función para actualizar la distancia máxima
function actualizarDistanciaMaxima(valor) {
    // Obtener el valor actual de la distancia mínima
    var distanciaMinima = parseInt(document.getElementById("distancia_minima").value);

    // Verificar si la distancia máxima es menor que la distancia mínima
    if (parseInt(valor) < distanciaMinima) {
        // Si la distancia máxima es menor que la distancia mínima, ajustar la distancia mínima
        document.getElementById("distancia_minima").value = valor;
        // Actualizar el valor mostrado para la distancia mínima
        document.getElementById("valor_distancia_minima").innerHTML = valor + " km";
    }

    // Actualizar el valor mostrado para la distancia máxima
    document.getElementById("valor_distancia_maxima").innerHTML = valor + " km";
}

// Función para actualizar la altura mínima
function actualizarAlturaMinima(valor) {
    // Obtener el valor actual de la altura máxima
    var alturaMaxima = parseInt(document.getElementById("altura_maxima").value);

    // Verificar si la altura mínima es mayor que la altura máxima
    if (parseInt(valor) > alturaMaxima) {
        // Si la altura mínima es mayor que la altura máxima, ajustar la altura máxima
        document.getElementById("altura_maxima").value = valor;
        // Actualizar el valor mostrado para la altura máxima
        document.getElementById("valor_altura_maxima").innerHTML = valor + " cm";
    }

    // Actualizar el valor mostrado para la altura mínima
    document.getElementById("valor_altura_minima").innerHTML = valor + " cm";
}

// Función para actualizar la altura máxima
function actualizarAlturaMaxima(valor) {
    // Obtener el valor actual de la altura mínima
    var alturaMinima = parseInt(document.getElementById("altura_minima").value);

    // Verificar si la altura máxima es menor que la altura mínima
    if (parseInt(valor) < alturaMinima) {
        // Si la altura máxima es menor que la altura mínima, ajustar la altura mínima
        document.getElementById("altura_minima").value = valor;
        // Actualizar el valor mostrado para la altura mínima
        document.getElementById("valor_altura_minima").innerHTML = valor + " cm";
    }

    // Actualizar el valor mostrado para la altura máxima
    document.getElementById("valor_altura_maxima").innerHTML = valor + " cm";
}

document.getElementById('religion').addEventListener('change', function() {
    var otherReligionInput = document.getElementById('other_religion');
    otherReligionInput.style.display = (this.value === 'otro') ? 'block' : 'none';
});

document.getElementById('relationship_type').addEventListener('change', function() {
    var otherRelationshipInput = document.getElementById('other_relationship');
    otherRelationshipInput.style.display = (this.value === 'otras') ? 'block' : 'none';
});