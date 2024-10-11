<template>
  <div>
    <p>Processing GitHub login...</p>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "~/stores/auth";
import { useRuntimeConfig } from "#app";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const config = useRuntimeConfig();

onMounted(async () => {
  const code = route.query.code;

  if (code) {
    try {
      const response = await fetch(
        `${config.public.apiBase}/api/v1/github/callback`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ code }),
        }
      );

      if (response.ok) {
        const data = await response.json();
        authStore.setToken(data.access_token);
        authStore.setUser(data.user);
        router.push("/generate-dashboard");
      } else {
        const errorData = await response.json();
        console.error("GitHub authentication error:", errorData);
        router.push(
          `/login?error=${encodeURIComponent(
            errorData.detail || "Authentication failed"
          )}`
        );
      }
    } catch (error) {
      console.error("GitHub authentication error:", error);
      router.push("/login?error=github_auth_failed");
    }
  } else {
    router.push("/login?error=no_code");
  }
});
</script>
