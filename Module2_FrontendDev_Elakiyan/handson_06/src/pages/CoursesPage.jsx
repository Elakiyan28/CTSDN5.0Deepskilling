import { useState } from "react";
import CourseCard from "../components/CourseCard.jsx";
import { initialCourses } from "../data.js";

export default function CoursesPage() {
  const [searchTerm, setSearchTerm] = useState("");

  const filtered = initialCourses.filter((c) =>
    c.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <section id="courses">
      <h2>Courses</h2>
      <input
        type="text"
        placeholder="Search courses..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <div className="course-grid">
        {filtered.map((course) => (
          <CourseCard key={course.id} {...course} />
        ))}
      </div>
    </section>
  );
}
