import { displayPage } from './navigation.js';

// Ejecuta la función una vez cargado el DOM
document.addEventListener('DOMContentLoaded', init);

const mainPage = 'home';

function init() {
    console.log('Initializing main...');
    displayPage(mainPage)
}