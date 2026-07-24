import { init as homeInit } from '../pages/home/home.js';
import { init as postInit } from '../pages/post/post.js';

export async function displayPage(page, postId = null) {
    const mainContent = document.getElementById('content');
    if (!mainContent) return;

    // obtener el contenido
    const response = await fetch(`pages/${page}/${page}.html`);
    const component = await response.text();

    // generar un html temporal
    const temp = document.createElement('div');
    temp.innerHTML = component;

    // obtener el template
    const template = temp.querySelector('template');

    // limpiar el contenido principal
    mainContent.innerHTML = '';

    // cargar la hoja de estilos
    displayStyles(page);

    // insertar el contenido
    mainContent.appendChild(template.content.cloneNode(true));

    // cargar la funcion init correspondiente
    switch (page) {
        case 'home': homeInit(); break;
        case 'post': postInit(postId); break;
    }
}

function displayStyles(page) {
    // Elimina los link de estilos generados dinamicamente
    document.querySelectorAll('link[data-page-style]').forEach(link => {
        link.remove();
    });

    // Crea la nueva hoja de estilos
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `pages/${page}/${page}.css`;
    link.dataset.pageStyle = page;

    // Inserta la hoja de estilos en el head del index
    document.head.appendChild(link);
}