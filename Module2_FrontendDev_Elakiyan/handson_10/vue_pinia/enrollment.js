import { defineStore } from "pinia";
import { ref } from "vue";
import { enrollStudent } from "../api/courseApi.js";

export const useEnrollmentStore = defineStore("enrollment", () => {
  const enrolledCourses = ref([]);
  const loading = ref(false);
  const error = ref(null);

  // Combines the API call and state update in one action
  async function fetchAndEnroll(studentId, course) {
    loading.value = true;
    error.value = null;
    try {
      await enrollStudent(studentId, course.id);
      enrolledCourses.value.push(course);
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }

  function $reset() {
    enrolledCourses.value = [];
    loading.value = false;
    error.value = null;
  }

  return { enrolledCourses, loading, error, fetchAndEnroll, $reset };
});

// Usage in a component, keeping reactivity when destructuring:
// import { storeToRefs } from "pinia";
// const store = useEnrollmentStore();
// const { enrolledCourses, loading } = storeToRefs(store); // reactive
// const { fetchAndEnroll } = store; // actions can be destructured directly

// Vue global error handler (Task 3 "for either framework"):
// app.config.errorHandler = (err, instance, info) => {
//   console.error("Global Vue error:", err, info);
// };
