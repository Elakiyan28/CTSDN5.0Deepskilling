export default function CourseCard({ id, name, code, credits, grade, onEnroll }) {
  return (
    <article className="course-card">
      <h3>{name}</h3>
      <p>{code}</p>
      <span>{credits} credits</span>
      <p className="grade">Grade: {grade}</p>
      <button onClick={() => onEnroll(id)}>Enroll</button>
    </article>
  );
}
