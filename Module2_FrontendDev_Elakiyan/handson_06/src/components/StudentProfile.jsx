import { useState } from "react";

export default function StudentProfile() {
  const [profile, setProfile] = useState({ name: "", email: "", semester: "" });

  function handleChange(e) {
    const { name, value } = e.target;
    setProfile((prev) => ({ ...prev, [name]: value }));
  }

  return (
    <section className="profile-form">
      <h2>Student Profile</h2>
      <label htmlFor="name">Name</label>
      <input id="name" name="name" value={profile.name} onChange={handleChange} />

      <label htmlFor="email">Email</label>
      <input id="email" name="email" type="email" value={profile.email} onChange={handleChange} />

      <label htmlFor="semester">Semester</label>
      <input id="semester" name="semester" type="number" value={profile.semester} onChange={handleChange} />

      <p>Preview: {profile.name} ({profile.email}) — Semester {profile.semester}</p>
    </section>
  );
}
