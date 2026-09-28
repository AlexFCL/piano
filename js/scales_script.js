const scales = [
    { label: 'C majeur', image: 'images/Scales/C-majeur.png', type: 'major' },
    { label: 'Db majeur', image: 'images/Scales/Db-majeur.png', type: 'major' },
    { label: 'D majeur', image: 'images/Scales/D-majeur.png', type: 'major' },
    { label: 'Eb majeur', image: 'images/Scales/Eb-majeur.png', type: 'major' },
    { label: 'E majeur', image: 'images/Scales/E-majeur.png', type: 'major' },
    { label: 'F majeur', image: 'images/Scales/F-majeur.png', type: 'major' },
    { label: 'F# majeur', image: 'images/Scales/Fd-majeur.png', type: 'major' },
    { label: 'G majeur', image: 'images/Scales/G-majeur.png', type: 'major' },
    { label: 'Ab majeur', image: 'images/Scales/Ab-majeur.png', type: 'major' },
    { label: 'A majeur', image: 'images/Scales/A-majeur.png', type: 'major' },
    { label: 'Bb majeur', image: 'images/Scales/Bb-majeur.png', type: 'major' },
    { label: 'B majeur', image: 'images/Scales/B-majeur.png', type: 'major' },
    { label: 'C mineure naturelle', image: 'images/Scales/C-mineur-naturel.png', type: 'minor' },
    { label: 'C# mineure naturelle', image: 'images/Scales/Cd-mineur-naturel.png', type: 'minor' },
    { label: 'D mineure naturelle', image: 'images/Scales/D-mineur-naturel.png', type: 'minor' },
    { label: 'Eb mineure naturelle', image: 'images/Scales/Eb-mineur-naturel.png', type: 'minor' },
    { label: 'E mineure naturelle', image: 'images/Scales/E-mineur-naturel.png', type: 'minor' },
    { label: 'F mineure naturelle', image: 'images/Scales/F-mineur-naturel.png', type: 'minor' },
    { label: 'F# mineure naturelle', image: 'images/Scales/Fd-mineur-naturel.png', type: 'minor' },
    { label: 'G mineure naturelle', image: 'images/Scales/G-mineur-naturel.png', type: 'minor' },
    { label: 'G# mineure naturelle', image: 'images/Scales/Gd-mineur-naturel.png', type: 'minor' },
    { label: 'A mineure naturelle', image: 'images/Scales/A-mineur-naturel.png', type: 'minor' },
    { label: 'Bb mineure naturelle', image: 'images/Scales/Bb-mineur-naturel.png', type: 'minor' },
    { label: 'B mineure naturelle', image: 'images/Scales/B-mineur-naturel.png', type: 'minor' }
];

const answerDuration = 3000;

const params = new URLSearchParams(window.location.search);
const parsedUpdateTime = Number.parseFloat(params.get('updateTime'));
let updateTime = Number.isFinite(parsedUpdateTime) && parsedUpdateTime >= 1 ? parsedUpdateTime : 5;

const scaleName = document.getElementById('scale-name');
const phaseLabel = document.getElementById('phase-label');
const scaleImage = document.getElementById('scale-image');
const imageError = document.getElementById('image-error');
const updateTimeInput = document.getElementById('scale-update-time');
const controlsHint = document.getElementById('scale-controls-hint');
const filterButtons = [...document.querySelectorAll('[data-scale-filter]')];

let previousImage = '';
let revealTimer;
let nextTimer;

updateTimeInput.value = String(updateTime);

function formatSeconds(value) {
    return Number.isInteger(value) ? String(value) : String(value).replace('.', ',');
}

function syncUpdateTime() {
    const parsed = Number.parseFloat(String(updateTimeInput.value).replace(',', '.'));

    if (Number.isFinite(parsed) && parsed >= 1) {
        updateTime = parsed;
        updateTimeInput.setAttribute('aria-invalid', 'false');
        controlsHint.textContent = `Temps réglé sur ${formatSeconds(updateTime)} s. Le changement s'appliquera à la prochaine gamme.`;
        return;
    }

    updateTimeInput.setAttribute('aria-invalid', 'true');
    controlsHint.textContent = 'Le temps de réponse doit être supérieur ou égal à 1 seconde.';
}

function setButtonState(button, isActive) {
    button.classList.toggle('is-active', isActive);
    button.setAttribute('aria-pressed', String(isActive));
}

filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const activeButtons = filterButtons.filter((candidate) => candidate.classList.contains('is-active'));

        if (button.classList.contains('is-active') && activeButtons.length === 1) {
            controlsHint.textContent = 'Garde au moins un type de gamme actif.';
            return;
        }

        setButtonState(button, !button.classList.contains('is-active'));
        controlsHint.textContent = 'Sélection mise à jour. Elle s’appliquera à la prochaine gamme.';
    });
});

updateTimeInput.addEventListener('input', syncUpdateTime);
updateTimeInput.addEventListener('change', syncUpdateTime);

function getActiveTypes() {
    return filterButtons
        .filter((button) => button.classList.contains('is-active'))
        .map((button) => button.dataset.scaleFilter);
}

function buildPool() {
    const activeTypes = getActiveTypes();
    return scales.filter((scale) => activeTypes.includes(scale.type));
}

function chooseScale() {
    const pool = buildPool();

    if (pool.length === 0) return null;

    if (pool.length === 1) {
        previousImage = pool[0].image;
        return pool[0];
    }

    let scale;
    do {
        scale = pool[Math.floor(Math.random() * pool.length)];
    } while (scale.image === previousImage);

    previousImage = scale.image;
    return scale;
}

function startRound() {
    clearTimeout(revealTimer);
    clearTimeout(nextTimer);

    const scale = chooseScale();
    if (!scale) return;

    const roundDelay = updateTime;

    scaleName.textContent = scale.label;
    phaseLabel.textContent = `À toi — réponse dans ${formatSeconds(roundDelay)} s`;
    scaleImage.hidden = true;
    scaleImage.removeAttribute('src');
    scaleImage.alt = `Réponse : ${scale.label}`;
    imageError.hidden = true;

    const preload = new Image();
    preload.src = scale.image;

    revealTimer = window.setTimeout(() => {
        scaleImage.src = scale.image;
        scaleImage.hidden = false;
        phaseLabel.textContent = 'Réponse';

        nextTimer = window.setTimeout(startRound, answerDuration);
    }, roundDelay * 1000);
}

scaleImage.addEventListener('error', () => {
    scaleImage.hidden = true;
    imageError.hidden = false;
});

startRound();
