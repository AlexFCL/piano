const roots = ["C", "D", "E", "F", "G", "A", "B", "C#", "Db", "D#", "Eb", "F#", "Gb", "G#", "Ab", "A#", "Bb"];

const qualities = {
    majeur: {
        displaySuffix: "",
        imageSlug: "majeur"
    },
    mineur: {
        displaySuffix: " mineur",
        imageSlug: "mineur"
    }
};

const inversions = {
    fond: {
        label: "fondamental",
        imageSlug: "fond"
    },
    "1er": {
        label: "1er renversement",
        imageSlug: "1er"
    },
    "2eme": {
        label: "2e renversement",
        imageSlug: "2eme"
    }
};

const answerDuration = 3000;

const updateTimeInput = document.getElementById("update-time");
const randomValuesElement = document.getElementById("random-values");
const phaseLabel = document.getElementById("phase-label");
const chordImage = document.getElementById("chord-image");
const imageError = document.getElementById("image-error");
const controlsHint = document.getElementById("controls-hint");
const filterButtons = [...document.querySelectorAll("[data-filter-group]")];

const params = new URLSearchParams(window.location.search);
const initialTime = Number.parseFloat(params.get("updateTime"));
let updateTime = Number.isFinite(initialTime) && initialTime >= 1 ? initialTime : 5;

let previousKey = "";
let revealTimer;
let nextTimer;

updateTimeInput.value = String(updateTime);

function formatSeconds(value) {
    return Number.isInteger(value) ? String(value) : String(value).replace(".", ",");
}

function syncUpdateTime() {
    const parsed = Number.parseFloat(String(updateTimeInput.value).replace(",", "."));

    if (Number.isFinite(parsed) && parsed >= 1) {
        updateTime = parsed;
        updateTimeInput.setAttribute("aria-invalid", "false");
        controlsHint.textContent = `Temps réglé sur ${formatSeconds(updateTime)} s. Le changement s'appliquera au prochain accord.`;
        return;
    }

    updateTimeInput.setAttribute("aria-invalid", "true");
    controlsHint.textContent = "Le temps de réponse doit être supérieur ou égal à 1 seconde.";
}

function getActiveValues(group) {
    return filterButtons
        .filter((button) => button.dataset.filterGroup === group && button.classList.contains("is-active"))
        .map((button) => button.dataset.value);
}

function setButtonState(button, isActive) {
    button.classList.toggle("is-active", isActive);
    button.setAttribute("aria-pressed", String(isActive));
}

filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
        const group = button.dataset.filterGroup;
        const activeInGroup = filterButtons.filter(
            (candidate) => candidate.dataset.filterGroup === group && candidate.classList.contains("is-active")
        );

        if (button.classList.contains("is-active") && activeInGroup.length === 1) {
            controlsHint.textContent = "Garde au moins une option active dans chaque catégorie.";
            return;
        }

        setButtonState(button, !button.classList.contains("is-active"));
        controlsHint.textContent = "Sélection mise à jour. Elle s'appliquera au prochain accord.";
    });
});

updateTimeInput.addEventListener("input", syncUpdateTime);
updateTimeInput.addEventListener("change", syncUpdateTime);

function buildPool() {
    const activeQualities = getActiveValues("quality");
    const activeInversions = getActiveValues("inversion");

    return roots.flatMap((root) =>
        activeQualities.flatMap((quality) =>
            activeInversions.map((inversion) => ({
                root,
                quality,
                inversion,
                key: `${root}|${quality}|${inversion}`
            }))
        )
    );
}

function chooseChord() {
    const pool = buildPool();

    if (pool.length === 0) {
        return null;
    }

    if (pool.length === 1) {
        previousKey = pool[0].key;
        return pool[0];
    }

    let chord;
    do {
        chord = pool[Math.floor(Math.random() * pool.length)];
    } while (chord.key === previousKey);

    previousKey = chord.key;
    return chord;
}

function getImagePath(chord) {
    const qualitySlug = qualities[chord.quality].imageSlug;
    const inversionSlug = inversions[chord.inversion].imageSlug;
    const imageName = `${chord.root}-${qualitySlug}-${inversionSlug}.png`;

    return `images/Chords/${encodeURIComponent(imageName)}`;
}

function renderQuestion(chord) {
    const quality = qualities[chord.quality];
    const inversion = inversions[chord.inversion];

    randomValuesElement.innerHTML = `
        <div class="random-value">
            ${chord.root}<span class="custom2">${quality.displaySuffix}</span>, ${inversion.label}
        </div>
    `;
}

function startRound() {
    clearTimeout(revealTimer);
    clearTimeout(nextTimer);

    const chord = chooseChord();
    if (!chord) return;

    const roundDelay = updateTime;
    const imagePath = getImagePath(chord);

    renderQuestion(chord);
    phaseLabel.textContent = `À toi — réponse dans ${formatSeconds(roundDelay)} s`;

    chordImage.hidden = true;
    chordImage.removeAttribute("src");
    chordImage.alt = `Réponse : ${chord.root} ${chord.quality}, ${inversions[chord.inversion].label}`;
    imageError.hidden = true;

    const preload = new Image();
    preload.src = imagePath;

    revealTimer = window.setTimeout(() => {
        chordImage.src = imagePath;
        chordImage.hidden = false;
        phaseLabel.textContent = "Réponse";

        nextTimer = window.setTimeout(startRound, answerDuration);
    }, roundDelay * 1000);
}

chordImage.addEventListener("error", () => {
    chordImage.hidden = true;
    imageError.hidden = false;
});

startRound();
