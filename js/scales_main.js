const input = document.getElementById('scale-update-time');
const startButton = document.getElementById('start-scales');

function startScaleTraining() {
    const updateTime = parseFloat(input.value.replace(',', '.'));

    if (!Number.isNaN(updateTime) && updateTime >= 1) {
        window.location.href = `scale_training.html?updateTime=${encodeURIComponent(updateTime)}`;
        return;
    }

    alert('Veuillez saisir un temps de réponse valide (un nombre supérieur ou égal à 1).');
}

startButton.addEventListener('click', startScaleTraining);
input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        startScaleTraining();
    }
});
