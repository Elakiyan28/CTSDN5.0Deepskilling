import { courses } from "./data.js";

// ===== Task 1: Promises and async/await =====

// .then() chain version
function fetchUser(id) {
  return fetch(`https://jsonplaceholder.typicode.com/users/${id}`)
    .then((res) => res.json())
    .then((user) => {
      console.log("fetchUser (.then):", user.name);
      return user;
    });
}

// async/await version of the same thing
async function fetchUserAsync(id) {
  try {
    const res = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
    const user = await res.json();
    console.log("fetchUserAsync:", user.name);
    return user;
  } catch (err) {
    console.error("fetchUserAsync failed:", err.message);
  }
}

fetchUser(1);
fetchUserAsync(1);

// Simulated network delay for local course data
function fetchAllCourses() {
  return new Promise((resolve) => {
    setTimeout(() => resolve(courses), 1000);
  });
}

async function loadCourses() {
  const courseGrid = document.querySelector(".course-grid");
  courseGrid.innerHTML = `<p class="loading">Loading courses...</p>`;

  const data = await fetchAllCourses();
  renderCourses(data);
}

// Promise.all demo: fetch two users simultaneously
async function fetchTwoUsers() {
  const [user1, user2] = await Promise.all([
    fetch("https://jsonplaceholder.typicode.com/users/1").then((r) => r.json()),
    fetch("https://jsonplaceholder.typicode.com/users/2").then((r) => r.json()),
  ]);
  console.log("Promise.all users:", user1.name, user2.name);
}
fetchTwoUsers();

// ===== Course rendering (carried over from Hands-On 3) =====

const courseGrid = document.querySelector(".course-grid");
const totalCreditsEl = document.getElementById("total-credits");

function renderCourses(list) {
  courseGrid.innerHTML = "";
  list.forEach((course) => {
    const article = document.createElement("article");
    article.className = "course-card";
    article.innerHTML = `
      <h3>${course.name}</h3>
      <p>${course.code}</p>
      <span>${course.credits} credits</span>
    `;
    courseGrid.appendChild(article);
  });
  const sum = list.reduce((s, c) => s + c.credits, 0);
  totalCreditsEl.textContent = `Total credits: ${sum}`;
}

loadCourses();

// ===== Task 2: Fetch API with Error Handling =====

async function apiFetch(url) {
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

const notificationsSection = document.getElementById("notifications");

async function loadNotifications(url = "https://jsonplaceholder.typicode.com/posts?_limit=5") {
  notificationsSection.innerHTML = `<p class="loading">Loading notifications...</p>`;

  try {
    const posts = await apiFetch(url);
    notificationsSection.innerHTML = posts
      .map(
        (p) => `
        <div class="notification-card">
          <h4>${p.title}</h4>
          <p>${p.body}</p>
        </div>`
      )
      .join("");
  } catch (err) {
    notificationsSection.innerHTML = `
      <div class="error-box">
        <p>Couldn't load notifications: ${err.message}</p>
        <button id="retry-btn">Retry</button>
      </div>`;
    document.getElementById("retry-btn").addEventListener("click", () => loadNotifications(url));
  }
}

loadNotifications();

// Button to demo the 404/error path on purpose
document.getElementById("break-fetch-btn").addEventListener("click", () => {
  loadNotifications("https://jsonplaceholder.typicode.com/nonexistent");
});

// ===== Task 3: Introduction to Axios =====
// axios is loaded globally via CDN script tag in index.html

axios.interceptors.request.use((config) => {
  console.log(`API call started: ${config.url}`);
  return config;
});

async function apiFetchAxios(url, params = {}) {
  // Axios auto-parses JSON and throws on non-2xx by default,
  // so no manual response.ok check is needed here.
  const res = await axios.get(url, { params, timeout: 5000 });
  return res.data;
}

async function loadUser1Posts() {
  try {
    const posts = await apiFetchAxios("https://jsonplaceholder.typicode.com/posts", { userId: 1 });
    console.log("User 1 posts via Axios:", posts.length);
  } catch (err) {
    console.error("Axios request failed:", err.message);
  }
}
loadUser1Posts();

/*
 Fetch vs Axios — 3 differences:
 1. Axios auto-parses JSON; fetch requires a manual .json() call.
 2. Axios rejects on any non-2xx status; fetch only rejects on network failure,
    so response.ok must be checked manually.
 3. Axios has built-in request/response interceptors and a timeout option;
    fetch needs AbortController + manual wrapping for the same behavior.
*/
