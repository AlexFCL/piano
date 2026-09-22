let scales = [];
let currentScale = null;
let currentAnswerNotes = [];

const params = new URLSearchParams(window.location.search);
const mode = params.get("mode") === "scale-from-any-note" ? "scale-from-any-note" : "scale-quiz";

const title = document.getElementById("quiz-title");
const question = document.getElementById("scale-question-text");
const inputsContainer = document.getElementById("notes-inputs");
const generateButton = document.getElementById("generate-scale-button");
const checkButton = document.getElementById("check-scale-button");

title.textContent = mode === "scale-from-any-note"
  ? "Construire depuis n’importe quelle note"
  : "Trouver les notes d’une gamme";

scales = await loadScales();

generateButton.addEventListener("click", generateRandomScale);
checkButton.addEventListener("click", checkAnswers);

async function loadScales() {
  const response = await fetch("data/music-theory/scales.json");
  const groupedScales = await response.json();
  return Object.entries(groupedScales).flatMap(([scaleType, items]) =>
    items.map(scale => ({ tonic: scale.tonic, scaleType, notes: scale.notes }))
  );
}

function generateRandomScale() {
  currentScale = scales[Math.floor(Math.random() * scales.length)];
  currentAnswerNotes = getAnswerNotes(currentScale);

  question.textContent = getQuestionText(currentScale, currentAnswerNotes);
  inputsContainer.innerHTML = currentAnswerNotes.map((note, index) => `
    <div class="note-field">
      <input class="note-input" type="text" maxlength="2" data-index="${index}" aria-label="Note ${index + 1}">
      <div class="note-correction"></div>
    </div>
  `).join("");

  const inputs = [...document.querySelectorAll(".note-input")];
  inputs.forEach(input => {
    input.addEventListener("input", () => {
      input.value = sanitizeNoteInput(input.value);
      input.classList.remove("is-correct", "is-wrong");
      input.parentElement.querySelector(".note-correction").textContent = "";

      if (input.value.length === input.maxLength) {
        focusNextInput(input, inputs);
      }
    });

    input.addEventListener("keydown", event => {
      if (event.key === " ") {
        event.preventDefault();
        focusNextInput(input, inputs);
      }
    });
  });

  checkButton.disabled = false;
  inputs[0]?.focus({ preventScroll: true });
}

function focusNextInput(currentInput, inputs) {
  const next = inputs[Number(currentInput.dataset.index) + 1];
  if (next) {
    next.focus({ preventScroll: true });
    next.select();
  }
}

function getAnswerNotes(scale) {
  if (mode !== "scale-from-any-note") return scale.notes;
  const startIndex = Math.floor(Math.random() * scale.notes.length);
  return [...scale.notes.slice(startIndex), ...scale.notes.slice(0, startIndex)];
}

function getQuestionText(scale, answerNotes) {
  if (mode !== "scale-from-any-note") {
    return `${scale.tonic} ${scale.scaleType}`;
  }
  return `${scale.tonic} ${scale.scaleType}, à partir de ${answerNotes[0]}`;
}

function checkAnswers() {
  if (!currentScale) return;

  document.querySelectorAll(".note-input").forEach(input => {
    const index = Number(input.dataset.index);
    const userAnswer = sanitizeNoteInput(input.value);
    const correctAnswer = currentAnswerNotes[index];
    const correction = input.parentElement.querySelector(".note-correction");

    input.value = userAnswer;
    input.classList.remove("is-correct", "is-wrong");

    if (userAnswer === correctAnswer) {
      input.classList.add("is-correct");
      correction.textContent = "";
    } else {
      input.classList.add("is-wrong");
      correction.textContent = correctAnswer;
    }
  });
}

function sanitizeNoteInput(value) {
  return normalizeNote(value).replace(/[^A-G#b]/g, "");
}

function normalizeNote(value) {
  const cleaned = value.trim();
  if (!cleaned) return "";

  const firstLetter = cleaned.charAt(0).toUpperCase();
  let accidental = cleaned.slice(1)
    .replace("d", "#")
    .replace("D", "#")
    .replace("B", "b");

  return firstLetter + accidental;
}
