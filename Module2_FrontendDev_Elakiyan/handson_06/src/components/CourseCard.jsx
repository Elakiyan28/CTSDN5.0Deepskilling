import { useDispatch } from "react-redux";
import { useNavigate, Link } from "react-router-dom";
import { enroll } from "../features/enrollmentSlice.js";

export default function CourseCard({ id, name, code, credits, grade }) {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  function handleEnroll() {
    dispatch(enroll({ id, name, code, credits, grade }));
    navigate("/profile");
  }

  return (
    <article className="course-card">
      <Link to={`/courses/${id}`}>
        <h3>{name}</h3>
        <p>{code}</p>
        <span>{credits} credits</span>
      </Link>
      <p className="grade">Grade: {grade}</p>
      <button onClick={handleEnroll}>Enroll</button>
    </article>
  );
}
