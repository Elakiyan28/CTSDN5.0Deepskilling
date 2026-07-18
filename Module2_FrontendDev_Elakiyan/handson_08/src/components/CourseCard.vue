<script setup>
defineProps({
  name: String,
  code: String,
  credits: Number,
  grade: String,
});
</script>

<template>
  <article class="course-card">
    <h3>{{ name }}</h3>
    <p>{{ code }}</p>
    <span>{{ credits }} credits</span>
    <p class="grade">Grade: {{ grade }}</p>
  </article>
</template>

<style scoped>
.course-card {
  padding: 20px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  background-color: #fff;
}
</style>
