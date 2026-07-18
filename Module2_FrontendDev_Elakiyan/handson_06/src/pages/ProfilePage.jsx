import { useSelector, useDispatch } from "react-redux";
import { unenroll } from "../features/enrollmentSlice.js";

export default function ProfilePage() {
  const enrolledCourses = useSelector((state) => state.enrollment.enrolledCourses);
  const dispatch = useDispatch();

  return (
    <section className="profile-page">
      <h2>My Enrolled Courses</h2>
      {enrolledCourses.length === 0 && <p>No courses enrolled yet.</p>}
      <ul>
        {enrolledCourses.map((c) => (
          <li key={c.id}>
            {c.name} ({c.credits} credits)
            <button onClick={() => dispatch(unenroll(c.id))}>Remove</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
