const response = await fetch("data/exercises/theorie.json");
const exercises = await response.json();

document.getElementById("theory-list").innerHTML = exercises.map(exercise => `
  <a class="menu-card" href="theory_quiz.html?mode=${encodeURIComponent(exercise.type)}">
    <div>
      <p class="card-kicker">Exercice</p>
      <h2>${exercise.title}</h2>
      <p>${exercise.description}</p>
    </div>
    <span>→</span>
  </a>
`).join("");
