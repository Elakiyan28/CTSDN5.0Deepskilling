import { useParams, Link } from "react-router-dom";
import { initialCourses } from "../data.js";

export default function CourseDetailPage() {
  const { courseId } = useParams();
  const course = initialCourses.find((c) => String(c.id) === courseId);

  if (!course) {
    return (
      <section>
        <p>Course not found.</p>
        <Link to="/courses">Back to Courses</Link>
      </section>
    );
  }

  return (
    <section className="course-detail">
      <h2>{course.name}</h2>
      <p>{course.code} — {course.credits} credits</p>
      <p>Grade: {course.grade}</p>
      <Link to="/courses">Back to Courses</Link>
    </section>
  );
}
