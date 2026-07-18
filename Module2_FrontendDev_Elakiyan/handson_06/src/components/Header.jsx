import { Link } from "react-router-dom";
import { useSelector } from "react-redux";

export default function Header({ siteName }) {
  const enrolledCount = useSelector((state) => state.enrollment.enrolledCourses.length);

  return (
    <header className="header">
      <div className="site-name">{siteName}</div>
      <nav aria-label="Main navigation">
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/courses">Courses</Link></li>
          <li><Link to="/profile">Profile ({enrolledCount})</Link></li>
        </ul>
      </nav>
    </header>
  );
}
