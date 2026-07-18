<script setup>
import { useEnrollmentStore } from "../stores/enrollment.js";

const store = useEnrollmentStore();
</script>

<template>
  <section class="profile-page">
    <h2>My Enrolled Courses</h2>
    <p v-if="store.enrolledCourses.length === 0">No courses enrolled yet.</p>
    <ul>
      <li v-for="c in store.enrolledCourses" :key="c.id">
        {{ c.name }} ({{ c.credits }} credits)
        <button @click="store.unenroll(c.id)">Remove</button>
      </li>
    </ul>
    <p><strong>Total credits: {{ store.totalCredits }}</strong></p>
  </section>
</template>
