const grid = document.getElementById("exercise-grid");

function createCategoryCard(category) {
  const link = document.createElement("a");
  link.className = "exercise-card";
  link.href = category.href;

  const icon = document.createElement("div");
  icon.className = "exercise-icon";
  icon.textContent = category.icon;
  icon.setAttribute("aria-hidden", "true");

  const copy = document.createElement("div");
  copy.className = "exercise-copy";

  const title = document.createElement("strong");
  title.textContent = category.title;

  const description = document.createElement("span");
  description.textContent = category.description;

  copy.append(title, description);

  const arrow = document.createElement("div");
  arrow.className = "exercise-arrow";
  arrow.textContent = "→";
  arrow.setAttribute("aria-hidden", "true");

  link.append(icon, copy, arrow);
  return link;
}

async function loadCategories() {
  try {
    const response = await fetch("data/categories.json");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const categories = await response.json();
    const fragment = document.createDocumentFragment();

    categories.forEach((category) => {
      fragment.appendChild(createCategoryCard(category));
    });

    grid.replaceChildren(fragment);
  } catch (error) {
    console.error("Impossible de charger les catégories :", error);
    grid.textContent = "Impossible de charger les exercices pour le moment.";
  }
}

loadCategories();
