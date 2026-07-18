<script setup>
import Header from "./components/Header.vue";
</script>

<template>
  <Header />
  <main>
    <RouterView />
  </main>
  <footer class="footer">
    <p>&copy; 2026 Student Portal. All rights reserved.</p>
  </footer>
</template>
