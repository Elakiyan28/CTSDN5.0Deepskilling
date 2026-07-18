import { courses } from "./data.js";

// ===== Task 1: ES6+ Syntax Practice =====

// Destructuring in a loop
for (const course of courses) {
  const { name, credits } = course;
  console.log(`${name} - ${credits} credits`);
}

// map: formatted strings
const formatted = courses.map(
  (c) => `${c.code} ${c.name} (${c.credits} credits)`
);
console.log("Formatted courses:", formatted);

// filter: credits >= 4
const heavyCourses = courses.filter((c) => c.credits >= 4);
console.log("Courses with 4+ credits:", heavyCourses.length);

// reduce: total credits
const totalCredits = courses.reduce((sum, c) => sum + c.credits, 0);
console.log("Total credits enrolled:", totalCredits);

// ===== Task 2: DOM Selection & Dynamic Rendering =====

const courseGrid = document.querySelector(".course-grid");
const totalCreditsEl = document.getElementById("total-credits");
const selectedCourseEl = document.getElementById("selected-course");

function renderCourses(list) {
  courseGrid.innerHTML = ""; // clear before re-render to avoid duplicates

  list.forEach((course) => {
    const article = document.createElement("article");
    article.className = "course-card";
    article.dataset.id = course.id;
    article.tabIndex = 0;

    article.innerHTML = `
      <h3>${course.name}</h3>
      <p>${course.code}</p>
      <span>${course.credits} credits</span>
    `;

    courseGrid.appendChild(article);
  });

  const sumCredits = list.reduce((sum, c) => sum + c.credits, 0);
  totalCreditsEl.textContent = `Total credits: ${sumCredits}`;
}

renderCourses(courses);

// ===== Task 3: Event Listeners & Interactivity =====

// Live search filter
const searchInput = document.getElementById("search-courses");
searchInput.addEventListener("input", (e) => {
  const term = e.target.value.toLowerCase();
  const filtered = courses.filter((c) => c.name.toLowerCase().includes(term));
  renderCourses(filtered);
});

// Sort by credits (descending)
const sortBtn = document.getElementById("sort-btn");
sortBtn.addEventListener("click", () => {
  const sorted = [...courses].sort((a, b) => b.credits - a.credits);
  renderCourses(sorted);
});

// Event delegation: single listener on the grid container
courseGrid.addEventListener("click", (e) => {
  const card = e.target.closest(".course-card");
  if (!card) return;

  const course = courses.find((c) => c.id === Number(card.dataset.id));
  if (course) {
    selectedCourseEl.textContent = `${course.name} — Grade: ${course.grade}`;
  }
});

// Also trigger selection via keyboard (Enter) since cards are focusable
courseGrid.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    const card = e.target.closest(".course-card");
    if (!card) return;
    const course = courses.find((c) => c.id === Number(card.dataset.id));
    if (course) {
      selectedCourseEl.textContent = `${course.name} — Grade: ${course.grade}`;
    }
  }
});
