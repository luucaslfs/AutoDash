<template>
  <nav class="bg-[var(--color-primary)] p-4 shadow-md">
    <div class="container mx-auto flex justify-between items-center">
      <NuxtLink to="/" class="text-2xl font-bold">AutoDash</NuxtLink>
      <div class="flex items-center space-x-4">
        <NuxtLink to="/" class="nav-link">Home</NuxtLink>
        <NuxtLink v-if="isAuthenticated" to="/generate-dashboard" class="nav-link">Generate Dashboard</NuxtLink>
        <NuxtLink v-if="!isAuthenticated" to="/login" class="btn-primary">Login</NuxtLink>
        <button v-else @click="logout" class="btn-secondary">Logout</button>
        <div v-if="isAuthenticated" class="flex items-center ml-4">
          <img :src="user?.avatar_url" alt="User Avatar" class="w-8 h-8 rounded-full mr-2" />
          <span class="text-[var(--color-text)]">{{ user?.name }}</span>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from "~/stores/auth";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
const { isAuthenticated, user } = storeToRefs(authStore);

const logout = () => {
  authStore.logout();
  navigateTo("/");
};
</script>

<style scoped>
.nav-link {
  @apply text-[var(--color-text)] hover:text-[var(--color-primary)] transition duration-300;
}
</style>