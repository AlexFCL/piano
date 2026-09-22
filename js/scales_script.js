const scales = [
    { label: 'C majeur', image: 'images/Scales/C-majeur.png' },
    { label: 'Db majeur', image: 'images/Scales/Db-majeur.png' },
    { label: 'D majeur', image: 'images/Scales/D-majeur.png' },
    { label: 'Eb majeur', image: 'images/Scales/Eb-majeur.png' },
    { label: 'E majeur', image: 'images/Scales/E-majeur.png' },
    { label: 'F majeur', image: 'images/Scales/F-majeur.png' },
    { label: 'F# majeur', image: 'images/Scales/Fd-majeur.png' },
    { label: 'G majeur', image: 'images/Scales/G-majeur.png' },
    { label: 'Ab majeur', image: 'images/Scales/Ab-majeur.png' },
    { label: 'A majeur', image: 'images/Scales/A-majeur.png' },
    { label: 'Bb majeur', image: 'images/Scales/Bb-majeur.png' },
    { label: 'B majeur', image: 'images/Scales/B-majeur.png' },
    { label: 'C mineure naturelle', image: 'images/Scales/C-mineur-naturel.png' },
    { label: 'C# mineure naturelle', image: 'images/Scales/Cd-mineur-naturel.png' },
    { label: 'D mineure naturelle', image: 'images/Scales/D-mineur-naturel.png' },
    { label: 'Eb mineure naturelle', image: 'images/Scales/Eb-mineur-naturel.png' },
    { label: 'E mineure naturelle', image: 'images/Scales/E-mineur-naturel.png' },
    { label: 'F mineure naturelle', image: 'images/Scales/F-mineur-naturel.png' },
    { label: 'F# mineure naturelle', image: 'images/Scales/Fd-mineur-naturel.png' },
    { label: 'G mineure naturelle', image: 'images/Scales/G-mineur-naturel.png' },
    { label: 'G# mineure naturelle', image: 'images/Scales/Gd-mineur-naturel.png' },
    { label: 'A mineure naturelle', image: 'images/Scales/A-mineur-naturel.png' },
    { label: 'Bb mineure naturelle', image: 'images/Scales/Bb-mineur-naturel.png' },
    { label: 'B mineure naturelle', image: 'images/Scales/B-mineur-naturel.png' }
];

const params = new URLSearchParams(window.location.search);
const parsedUpdateTime = Number.parseFloat(params.get('updateTime'));
const updateTime = Number.isFinite(parsedUpdateTime) && parsedUpdateTime >= 1 ? parsedUpdateTime : 5;
const answerDuration = 3000;

const scaleName = document.getElementById('scale-name');
const phaseLabel = document.getElementById('phase-label');
const scaleImage = document.getElementById('scale-image');
const imageError = document.getElementById('image-error');
const responseTimeValue = document.getElementById('response-time-value');

let previousIndex = -1;
let revealTimer;
let nextTimer;

responseTimeValue.textContent = `${updateTime} s`;

function chooseScaleIndex() {
    if (scales.length < 2) return 0;

    let index;
    do {
        index = Math.floor(Math.random() * scales.length);
    } while (index === previousIndex);

    previousIndex = index;
    return index;
}

function startRound() {
    clearTimeout(revealTimer);
    clearTimeout(nextTimer);

    const scale = scales[chooseScaleIndex()];

    scaleName.textContent = scale.label;
    phaseLabel.textContent = `À toi — réponse dans ${updateTime} s`;
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
    }, updateTime * 1000);
}

scaleImage.addEventListener('error', () => {
    scaleImage.hidden = true;
    imageError.hidden = false;
});

startRound();
