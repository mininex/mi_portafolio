document.addEventListener("DOMContentLoaded", function() {
    const formulario = document.getElementById('formulario-recomendacion');
    const contenedorRecomendaciones = document.querySelector('.contenedor-recomendaciones');
    const mensajeConfirmacion = document.getElementById('mensaje-confirmacion');

    formulario.addEventListener('submit', function(event) {
        event.preventDefault(); // Evita que la página se recargue

        const nombre = document.getElementById('nombre').value;
        const recomendacionTexto = document.getElementById('recomendacion').value;

        if (nombre && recomendacionTexto) {
            // Crea un nuevo elemento para la recomendación
            const nuevaRecomendacion = document.createElement('div');
            nuevaRecomendacion.classList.add('recomendacion-item');
            nuevaRecomendacion.innerHTML = `
                <p>"${recomendacionTexto}"</p>
                <p class="autor">- ${nombre}</p>
            `;

            // Añade la nueva recomendación a la lista existente
            contenedorRecomendaciones.appendChild(nuevaRecomendacion);

            // Muestra el mensaje de confirmación
            mensajeConfirmacion.style.display = 'block';

            // Oculta el mensaje después de 3 segundos
            setTimeout(function() {
                mensajeConfirmacion.style.display = 'none';
            }, 3000);

            // Limpia el formulario
            formulario.reset();
        }
    });
});