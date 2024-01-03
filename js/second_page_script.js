/* Fichier JavaScript de la seconde page */

const list1 = ["C", "D", "E", "F", "G", "A", "B", "C#", "Db", "D#", "Eb", "F#", "Gb", "G#", "Ab", "A#", "Bb"];
const list2 = ["", " min"];
const list3 = [", fond.", ", 1er (tonique haut)", ", 2ème (tierce haut)"];

const urlParams = new URLSearchParams(window.location.search);
const updateTime = urlParams.get('updateTime') || 5;

function getRandomValues() {
    const randomValue1 = list1[Math.floor(Math.random() * list1.length)];
    const randomValue2 = list2[Math.floor(Math.random() * list2.length)];
    const randomValue3 = list3[Math.floor(Math.random() * list3.length)];

    return [randomValue1, randomValue2, randomValue3];
}

function updateRandomValues() {
    const [value1, value2, value3] = getRandomValues();

    const randomValuesElement = document.getElementById('random-values');
    randomValuesElement.innerHTML = `<div class="random-value">${value1}<span class="custom2">${value2}</span></div>`;

    const chordImage = document.getElementById('chord-image');
    const imageName = `${list1.indexOf(value1)}-${list2.indexOf(value2)}-${list3.indexOf(value3)}.jpg`;
    chordImage.src = `images/${imageName}`;

    setTimeout(updateRandomValues, updateTime * 1000);
}

updateRandomValues();
