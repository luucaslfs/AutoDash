<template>
  <div class="bg-white min-h-screen">
    <div class="container mx-auto px-4 py-16">
      <!-- Hero Section -->
      <div class="text-center mb-16">
        <h1 class="text-4xl font-bold text-[var(--color-primary)] mb-4">Welcome to AutoDash</h1>
        <p class="text-xl text-gray-600 mb-8">Democratizing data visualization through AI-powered dashboard generation</p>
        <div v-if="isAuthenticated">
          <p class="text-lg text-gray-700 mb-4">Hello, {{ user?.name || "User" }}! You're logged in.</p>
          <NuxtLink to="/generate-dashboard" class="btn-primary">
            Generate Dashboard
          </NuxtLink>
        </div>
        <div v-else>
          <p class="text-lg text-gray-700 mb-4">Please log in to use AutoDash.</p>
          <NuxtLink to="/login" class="btn-primary">
            Login
          </NuxtLink>
        </div>
      </div>

      <!-- Features Section -->
      <div class="grid md:grid-cols-3 gap-8 mb-16">
        <div class="bg-gray-100 p-6 rounded-lg">
          <h2 class="text-xl font-semibold text-[var(--color-secondary)] mb-4">AI-Powered Dashboard Creation</h2>
          <p class="text-gray-600">Our AI assistant automatically generates personalized dashboards from your data, making data visualization accessible to users of all skill levels.</p>
        </div>
        <div class="bg-gray-100 p-6 rounded-lg">
          <h2 class="text-xl font-semibold text-[var(--color-secondary)] mb-4">Intelligent Data Analysis</h2>
          <p class="text-gray-600">Our AI identifies the most relevant data points and suggests the best visualizations based on your dataset, ensuring accurate and meaningful insights.</p>
        </div>
        <div class="bg-gray-100 p-6 rounded-lg">
          <h2 class="text-xl font-semibold text-[var(--color-secondary)] mb-4">GitHub Integration</h2>
          <p class="text-gray-600">Seamlessly save your generated dashboard code as a GitHub repository, facilitating easy sharing and collaboration with your team.</p>
        </div>
      </div>

      <!-- Benefits Section -->
      <div class="text-center mb-16">
        <h2 class="text-3xl font-bold text-[var(--color-secondary)] mb-8">Why Choose AutoDash?</h2>
        <ul class="text-left max-w-2xl mx-auto">
          <li class="flex items-center mb-4">
            <span class="text-green-500 mr-2">✓</span>
            <span class="text-gray-700">Reduce time and effort in creating data visualizations</span>
          </li>
          <li class="flex items-center mb-4">
            <span class="text-green-500 mr-2">✓</span>
            <span class="text-gray-700">Generate insights quickly, even without extensive technical knowledge</span>
          </li>
          <li class="flex items-center mb-4">
            <span class="text-green-500 mr-2">✓</span>
            <span class="text-gray-700">Improve decision-making with accurate and relevant data representations</span>
          </li>
          <li class="flex items-center">
            <span class="text-green-500 mr-2">✓</span>
            <span class="text-gray-700">Intuitive interface for easy interaction and customization</span>
          </li>
        </ul>
      </div>

      <!-- Call to Action -->
      <div class="text-center">
        <h2 class="text-3xl font-bold text-[var(--color-secondary)] mb-4">Ready to transform your data?</h2>
        <p class="text-xl text-gray-600 mb-8">Join AutoDash today and unlock the power of your data!</p>
        <NuxtLink to="/signup" class="btn-secondary">
          Sign Up Now
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "~/stores/auth";
import { storeToRefs } from "pinia";

const authStore = useAuthStore();
const { isAuthenticated, user } = storeToRefs(authStore);
</script>

<style scoped>
.btn-primary {
  @apply bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded transition duration-300;
}

.btn-secondary {
  @apply bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition duration-300;
}
</style>