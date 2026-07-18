import apiClient from "./apiClient.js";

// Note: JSONPlaceholder doesn't have a real "courses" resource, so /posts
// stands in for it here, same as earlier hands-ons.

export function getAllCourses() {
  return apiClient.get("/posts?_limit=5");
}

export function getCourseById(id) {
  return apiClient.get(`/posts/${id}`);
}

export function enrollStudent(studentId, courseId) {
  return apiClient.post("/enrollments", { studentId, courseId });
}
