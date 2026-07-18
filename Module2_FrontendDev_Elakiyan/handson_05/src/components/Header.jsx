export default function Header({ siteName, enrolledCount }) {
  return (
    <header className="header">
      <div className="site-name">{siteName}</div>
      <nav aria-label="Main navigation">
        <ul>
          <li><a href="#home">Home</a></li>
          <li><a href="#courses">Courses</a></li>
          <li><a href="#profile">Profile ({enrolledCount})</a></li>
        </ul>
      </nav>
    </header>
  );
}
