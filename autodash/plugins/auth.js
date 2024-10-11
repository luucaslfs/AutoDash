import { useAuthStore } from "~/stores/auth";

export default defineNuxtPlugin((nuxtApp) => {
  if (import.meta.client) {
    const authStore = useAuthStore(nuxtApp.$pinia);

    // Initialize auth state
    authStore.initializeFromStorage();
  }
});
