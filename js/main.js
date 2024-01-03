/* Fichier JavaScript principal */

function saveUpdateTime() {
    const updateTimeInput = document.getElementById('update-time');
    const updateTime = parseFloat(updateTimeInput.value.replace(',', '.'));

    if (!isNaN(updateTime) && updateTime >= 1) {
        window.location.href = `second_page.html?updateTime=${updateTime}`;
    } else {
        alert('Veuillez saisir un temps d\'actualisation valide (un nombre supérieur ou égal à 1).');
    }
}
