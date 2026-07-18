import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  fetchAllCourses,
  selectCourses,
  selectCoursesLoading,
  selectCoursesError,
} from "../features/coursesSlice.js";

export default function CoursesPage() {
  const dispatch = useDispatch();
  const courses = useSelector(selectCourses);
  const loading = useSelector(selectCoursesLoading);
  const error = useSelector(selectCoursesError);

  useEffect(() => {
    dispatch(fetchAllCourses());
  }, [dispatch]);

  if (loading) return <p className="loading">Loading courses...</p>;
  if (error) return <p className="error">Error: {error}</p>;

  return (
    <section id="courses">
      <h2>Courses</h2>
      <div className="course-grid">
        {courses.map((c) => (
          <article key={c.id} className="course-card">
            <h3>{c.title}</h3>
          </article>
        ))}
      </div>
    </section>
  );
}
