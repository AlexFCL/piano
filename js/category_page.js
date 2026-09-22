const params = new URLSearchParams(window.location.search);
const category = params.get("category");

const config = {
  basse: {
    title: "Basse",
    description: "Technique, grooves et endurance",
    file: "data/exercises/basse.json"
  },
  rythme: {
    title: "Rythme",
    description: "Placement, lecture rythmique et précision",
    file: "data/exercises/rythme.json"
  }
};

const current = config[category];

if (!current) {
  window.location.replace("index.html");
} else {
  document.title = `Exercices — ${current.title}`;
  document.getElementById("category-title").textContent = current.title;
  document.getElementById("category-description").textContent = current.description;
  document.getElementById("category-eyebrow").textContent = `${current.title} · entraînement`;

  const response = await fetch(current.file);
  const exercises = await response.json();

  document.getElementById("exercise-list").innerHTML = exercises.map(exercise => `
    <article class="instruction-card">
      <p class="card-kicker">Exercice</p>
      <h2>${exercise.title}</h2>
      <p>${exercise.description}</p>
      ${exercise.duration ? `<span class="duration-pill">${exercise.duration}</span>` : ""}
    </article>
  `).join("");
}
