const params = new URLSearchParams(window.location.search);
const category = params.get("category");

try {
  const categoriesResponse = await fetch("data/categories.json");
  if (!categoriesResponse.ok) {
    throw new Error(`HTTP ${categoriesResponse.status}`);
  }

  const categories = await categoriesResponse.json();
  const current = categories.find(item => item.id === category && item.exerciseFile);

  if (!current) {
    window.location.replace("index.html");
  } else {
    document.title = `Exercices — ${current.title}`;
    document.getElementById("category-title").textContent = current.title;
    document.getElementById("category-description").textContent = current.description;
    document.getElementById("category-eyebrow").textContent = `${current.title} · entraînement`;

    const response = await fetch(current.exerciseFile);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

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
} catch (error) {
  console.error("Impossible de charger la catégorie :", error);
  document.getElementById("exercise-list").textContent = "Impossible de charger les exercices pour le moment.";
}
