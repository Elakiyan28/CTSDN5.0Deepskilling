import { useState, useEffect } from "react";
import Header from "./components/Header.jsx";
import Footer from "./components/Footer.jsx";
import CourseCard from "./components/CourseCard.jsx";
import StudentProfile from "./components/StudentProfile.jsx";

export default function App() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [enrolledCourses, setEnrolledCourses] = useState([]);

  // Fetch courses from JSONPlaceholder on mount, mapped to course-like shape
  useEffect(() => {
    async function loadCourses() {
      try {
        setLoading(true);
        const res = await fetch("https://jsonplaceholder.typicode.com/posts?_limit=5");
        if (!res.ok) throw new Error(`Failed to load courses: ${res.status}`);
        const posts = await res.json();

        const mapped = posts.map((p, i) => ({
          id: p.id,
          name: p.title.slice(0, 24),
          code: `CS${100 + i}`,
          credits: 3 + (i % 2),
          grade: ["A", "A-", "B+", "B", "A"][i],
        }));

        setCourses(mapped);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    loadCourses();
  }, []); // empty array = run once on mount, like componentDidMount

  // Runs whenever `courses` changes. The dependency array here matters:
  // without it, this effect would run after every render (including the
  // setCourses call above it triggers), causing an infinite loop.
  useEffect(() => {
    console.log("Courses updated");
  }, [courses]);

  function handleEnroll(courseId) {
    const course = courses.find((c) => c.id === courseId);
    if (course && !enrolledCourses.some((c) => c.id === courseId)) {
      setEnrolledCourses((prev) => [...prev, course]);
    }
  }

  const filteredCourses = courses.filter((c) =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />

      <main>
        <section id="courses">
          <h2>Courses</h2>

          <input
            type="text"
            placeholder="Search courses..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />

          {loading && <p className="loading">Loading...</p>}
          {error && <p className="error">Error: {error}</p>}

          <div className="course-grid">
            {!loading &&
              !error &&
              filteredCourses.map((course) => (
                <CourseCard key={course.id} {...course} onEnroll={handleEnroll} />
              ))}
          </div>
        </section>

        <StudentProfile />
      </main>

      <Footer />
    </>
  );
}
