// Task 2 deliverable: Context API version of enrollment state.
// Task 3 replaces this with Redux Toolkit (see store.js / features/enrollmentSlice.js).
// Kept here to show the "before" state and how prop-drilling was solved
// before the Redux refactor.

import { createContext, useState } from "react";

export const EnrollmentContext = createContext(null);

export function EnrollmentProvider({ children }) {
  const [enrolledCourses, setEnrolledCourses] = useState([]);

  function enrollCourse(course) {
    setEnrolledCourses((prev) =>
      prev.some((c) => c.id === course.id) ? prev : [...prev, course]
    );
  }

  function removeCourse(courseId) {
    setEnrolledCourses((prev) => prev.filter((c) => c.id !== courseId));
  }

  return (
    <EnrollmentContext.Provider value={{ enrolledCourses, enrollCourse, removeCourse }}>
      {children}
    </EnrollmentContext.Provider>
  );
}
