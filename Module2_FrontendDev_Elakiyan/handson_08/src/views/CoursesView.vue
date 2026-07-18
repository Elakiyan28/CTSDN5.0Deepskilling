<script setup>
import { ref, computed, onMounted } from "vue";
import CourseCard from "../components/CourseCard.vue";
import { useEnrollmentStore } from "../stores/enrollment.js";
import { useRouter } from "vue-router";
import { courses as courseData } from "../data.js";

const courses = ref([]);
const searchTerm = ref("");
const store = useEnrollmentStore();
const router = useRouter();

onMounted(() => {
  courses.value = courseData;
});

const filteredCourses = computed(() =>
  courses.value.filter((c) => c.name.toLowerCase().includes(searchTerm.value.toLowerCase()))
);

function handleEnroll(course) {
  store.enroll(course);
  router.push("/profile");
}
</script>

<template>
  <section id="courses">
    <h2>Courses</h2>
    <input type="text" v-model="searchTerm" placeholder="Search courses..." />

    <div class="course-grid">
      <div v-for="course in filteredCourses" :key="course.id">
        <RouterLink :to="`/courses/${course.id}`">
          <CourseCard :name="course.name" :code="course.code" :credits="course.credits" :grade="course.grade" />
        </RouterLink>
        <button @click="handleEnroll(course)">Enroll</button>
      </div>
    </div>
  </section>
</template>
