import { courses } from "./data.js";

const courseGrid = document.querySelector(".course-grid");
const totalCreditsEl = document.getElementById("total-credits");
const selectedCourseEl = document.getElementById("selected-course");
const resultsCountEl = document.getElementById("results-count");

function renderCourses(list) {
  courseGrid.innerHTML = "";

  list.forEach((course) => {
    const article = document.createElement("article");
    article.className = "course-card";
    article.dataset.id = course.id;
    article.tabIndex = 0; // keyboard-focusable

    article.innerHTML = `
      <h3>${course.name}</h3>
      <p>${course.code}</p>
      <span>${course.credits} credits</span>
    `;

    courseGrid.appendChild(article);
  });

  const sumCredits = list.reduce((sum, c) => sum + c.credits, 0);
  totalCreditsEl.textContent = `Total credits: ${sumCredits}`;

  // aria-live="polite" region: announces the new count to screen readers
  // without interrupting whatever they're currently reading.
  resultsCountEl.textContent = `${list.length} course${list.length === 1 ? "" : "s"} found`;
}

renderCourses(courses);

// Search
document.getElementById("search-courses").addEventListener("input", (e) => {
  const term = e.target.value.toLowerCase();
  renderCourses(courses.filter((c) => c.name.toLowerCase().includes(term)));
});

// Sort
document.getElementById("sort-btn").addEventListener("click", () => {
  renderCourses([...courses].sort((a, b) => b.credits - a.credits));
});

// Click + keyboard (Enter) selection via event delegation
function selectCourse(target) {
  const card = target.closest(".course-card");
  if (!card) return;
  const course = courses.find((c) => c.id === Number(card.dataset.id));
  if (course) {
    selectedCourseEl.textContent = `${course.name} — Grade: ${course.grade}`;
  }
}

courseGrid.addEventListener("click", (e) => selectCourse(e.target));
courseGrid.addEventListener("keydown", (e) => {
  if (e.key === "Enter") selectCourse(e.target);
});

// Hamburger: toggle aria-expanded + visible nav list
const hamburgerBtn = document.getElementById("hamburger-btn");
const navList = document.querySelector("header nav ul");

hamburgerBtn.addEventListener("click", () => {
  const isOpen = hamburgerBtn.getAttribute("aria-expanded") === "true";
  hamburgerBtn.setAttribute("aria-expanded", String(!isOpen));
  navList.classList.toggle("open", !isOpen);
});
