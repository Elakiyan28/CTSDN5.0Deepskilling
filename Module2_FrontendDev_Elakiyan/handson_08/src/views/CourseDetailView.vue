<script setup>
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { courses } from "../data.js";
import { useEnrollmentStore } from "../stores/enrollment.js";

const route = useRoute();
const router = useRouter();
const store = useEnrollmentStore();

const course = computed(() => courses.find((c) => String(c.id) === route.params.id));

function handleEnroll() {
  if (course.value) {
    store.enroll(course.value);
    router.push("/profile");
  }
}
</script>

<template>
  <section v-if="course" class="course-detail">
    <h2>{{ course.name }}</h2>
    <p>{{ course.code }} — {{ course.credits }} credits</p>
    <p>Grade: {{ course.grade }}</p>
    <button @click="handleEnroll">Enroll</button>
  </section>
  <p v-else>Course not found.</p>
</template>
