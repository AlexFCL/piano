/* Fichier JavaScript de la seconde page */

const list1 = ["C", "D", "E", "F", "G", "A", "B", "C#", "Db", "D#", "Eb", "F#", "Gb", "G#", "Ab", "A#", "Bb"];
const list2 = ["", " min"];
const list3 = ["fond.", "1er (tonique haut)", "2ème (tierce haut)"];
const inversionSlugs = ["fond", "1er", "2eme"];

const urlParams = new URLSearchParams(window.location.search);
const updateTime = urlParams.get('updateTime') || 5;

const responseTimeValue = document.getElementById('response-time-value');
if (responseTimeValue) {
    responseTimeValue.textContent = `${updateTime} s`;
}

function getRandomValues() {
    const randomValue1 = list1[Math.floor(Math.random() * list1.length)];
    const randomValue2 = list2[Math.floor(Math.random() * list2.length)];
    const randomValue3 = list3[Math.floor(Math.random() * list3.length)];

    return [randomValue1, randomValue2, randomValue3];
}

function updateRandomValues() {
    const [value1, value2, value3] = getRandomValues();

    const randomValuesElement = document.getElementById('random-values');
    randomValuesElement.innerHTML = `<div class="random-value">${value1}<span class="custom2">${value2}</span><span class="custom3">${value3}</span></div>`;

    const chordImage = document.getElementById('chord-image');
    const qualitySlug = value2 === "" ? "majeur" : "mineur";
    const inversionSlug = inversionSlugs[list3.indexOf(value3)];
    const imageName = `${value1}-${qualitySlug}-${inversionSlug}.png`;

    // encodeURIComponent is required for sharp spellings such as C# / F# / G#.
    chordImage.src = `images/Chords/${encodeURIComponent(imageName)}`;

    setTimeout(updateRandomValues, updateTime * 1000);
}

updateRandomValues();
