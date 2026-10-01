const scales = [
    { root: 'C', type: 'major', label: 'C majeur', image: 'images/Scales/C-majeur.png' },
    { root: 'Db', type: 'major', label: 'Db majeur', image: 'images/Scales/Db-majeur.png' },
    { root: 'D', type: 'major', label: 'D majeur', image: 'images/Scales/D-majeur.png' },
    { root: 'Eb', type: 'major', label: 'Eb majeur', image: 'images/Scales/Eb-majeur.png' },
    { root: 'E', type: 'major', label: 'E majeur', image: 'images/Scales/E-majeur.png' },
    { root: 'F', type: 'major', label: 'F majeur', image: 'images/Scales/F-majeur.png' },
    { root: 'F#', type: 'major', label: 'F# majeur', image: 'images/Scales/Fd-majeur.png' },
    { root: 'G', type: 'major', label: 'G majeur', image: 'images/Scales/G-majeur.png' },
    { root: 'Ab', type: 'major', label: 'Ab majeur', image: 'images/Scales/Ab-majeur.png' },
    { root: 'A', type: 'major', label: 'A majeur', image: 'images/Scales/A-majeur.png' },
    { root: 'Bb', type: 'major', label: 'Bb majeur', image: 'images/Scales/Bb-majeur.png' },
    { root: 'B', type: 'major', label: 'B majeur', image: 'images/Scales/B-majeur.png' },
    { root: 'C', type: 'minor', label: 'C mineure naturelle', image: 'images/Scales/C-mineur-naturel.png' },
    { root: 'C#', type: 'minor', label: 'C# mineure naturelle', image: 'images/Scales/Cd-mineur-naturel.png' },
    { root: 'D', type: 'minor', label: 'D mineure naturelle', image: 'images/Scales/D-mineur-naturel.png' },
    { root: 'Eb', type: 'minor', label: 'Eb mineure naturelle', image: 'images/Scales/Eb-mineur-naturel.png' },
    { root: 'E', type: 'minor', label: 'E mineure naturelle', image: 'images/Scales/E-mineur-naturel.png' },
    { root: 'F', type: 'minor', label: 'F mineure naturelle', image: 'images/Scales/F-mineur-naturel.png' },
    { root: 'F#', type: 'minor', label: 'F# mineure naturelle', image: 'images/Scales/Fd-mineur-naturel.png' },
    { root: 'G', type: 'minor', label: 'G mineure naturelle', image: 'images/Scales/G-mineur-naturel.png' },
    { root: 'G#', type: 'minor', label: 'G# mineure naturelle', image: 'images/Scales/Gd-mineur-naturel.png' },
    { root: 'A', type: 'minor', label: 'A mineure naturelle', image: 'images/Scales/A-mineur-naturel.png' },
    { root: 'Bb', type: 'minor', label: 'Bb mineure naturelle', image: 'images/Scales/Bb-mineur-naturel.png' },
    { root: 'B', type: 'minor', label: 'B mineure naturelle', image: 'images/Scales/B-mineur-naturel.png' }
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
const typeButtons = [...document.querySelectorAll('[data-scale-filter]')];
const rootButtons = [...document.querySelectorAll('[data-scale-root]')];

let previousImage = '';
let revealTimer;
let nextTimer;
let selectionEmpty = false;

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

function getActiveTypes() {
    return typeButtons
        .filter((button) => button.classList.contains('is-active'))
        .map((button) => button.dataset.scaleFilter);
}

function getActiveRoots() {
    const values = rootButtons
        .filter((button) => button.classList.contains('is-active'))
        .map((button) => button.dataset.scaleRoot);

    return values.includes('all') ? null : values;
}

function buildPool() {
    const activeTypes = getActiveTypes();
    const activeRoots = getActiveRoots();

    return scales.filter((scale) =>
        activeTypes.includes(scale.type) &&
        (activeRoots === null || activeRoots.includes(scale.root))
    );
}

function showEmptySelection() {
    clearTimeout(revealTimer);
    clearTimeout(nextTimer);
    selectionEmpty = true;
    previousImage = '';

    scaleName.textContent = 'Aucune gamme disponible';
    phaseLabel.textContent = 'Modifie les filtres';
    scaleImage.hidden = true;
    scaleImage.removeAttribute('src');
    imageError.hidden = true;
    controlsHint.textContent = 'Cette combinaison de tonique et de type de gamme n’existe pas dans les gammes disponibles.';
}

function applySelectionChange(message) {
    if (buildPool().length === 0) {
        showEmptySelection();
        return;
    }

    controlsHint.textContent = message;

    if (selectionEmpty) {
        selectionEmpty = false;
        startRound();
    }
}

typeButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const activeButtons = typeButtons.filter((candidate) => candidate.classList.contains('is-active'));

        if (button.classList.contains('is-active') && activeButtons.length === 1) {
            controlsHint.textContent = 'Garde au moins un type de gamme actif.';
            return;
        }

        setButtonState(button, !button.classList.contains('is-active'));
        applySelectionChange('Sélection mise à jour. Elle s’appliquera à la prochaine gamme.');
    });
});

rootButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const allButton = rootButtons.find((candidate) => candidate.dataset.scaleRoot === 'all');

        if (button.dataset.scaleRoot === 'all') {
            rootButtons.forEach((candidate) => setButtonState(candidate, candidate === allButton));
            applySelectionChange('Toutes les toniques sont actives. Le changement s’appliquera à la prochaine gamme.');
            return;
        }

        if (allButton && allButton.classList.contains('is-active')) {
            setButtonState(allButton, false);
            setButtonState(button, true);
            applySelectionChange(`Tonique ${button.dataset.scaleRoot} sélectionnée. Le changement s’appliquera à la prochaine gamme.`);
            return;
        }

        const activeRoots = rootButtons.filter(
            (candidate) => candidate.dataset.scaleRoot !== 'all' && candidate.classList.contains('is-active')
        );

        if (button.classList.contains('is-active') && activeRoots.length === 1) {
            controlsHint.textContent = 'Garde au moins une tonique active, ou choisis « Toutes ».';
            return;
        }

        setButtonState(button, !button.classList.contains('is-active'));
        applySelectionChange('Sélection des toniques mise à jour. Elle s’appliquera à la prochaine gamme.');
    });
});

updateTimeInput.addEventListener('input', syncUpdateTime);
updateTimeInput.addEventListener('change', syncUpdateTime);

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
    if (!scale) {
        showEmptySelection();
        return;
    }

    selectionEmpty = false;
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
