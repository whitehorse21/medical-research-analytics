<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue';
import { useTheme } from './composables/useTheme';

// Ensure theme is initialized when app mounts
const { initTheme } = useTheme();

onMounted(() => {
  // Re-initialize theme to ensure it's applied
  initTheme();
});
</script>
