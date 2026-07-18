<script setup>
import { useEnrollmentStore } from "../stores/enrollment.js";

const store = useEnrollmentStore();
</script>

<template>
  <header class="header">
    <div class="site-name">Student Portal</div>
    <nav aria-label="Main navigation">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/courses">Courses</RouterLink>
      <RouterLink to="/profile">Profile ({{ store.enrolledCourses.length }})</RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: #1e293b;
  color: #fff;
}
nav a {
  color: #fff;
  text-decoration: none;
  margin-left: 20px;
}
</style>
