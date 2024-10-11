<template>
  <div class="login-container">
    <h1>Welcome to AutoDash</h1>
    <button @click="loginWithGitHub" class="github-button">
      Login with GitHub
    </button>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRuntimeConfig } from "nuxt/app";

const config = useRuntimeConfig();
const error = ref("");

const loginWithGitHub = () => {
  const githubClientId = config.public.githubClientId;
  const redirectUri = encodeURIComponent(
    `${window.location.origin}/github/callback`
  );
  //const state = Math.random().toString(36).substring(7);
  const githubAuthUrl = `https://github.com/login/oauth/authorize?client_id=${githubClientId}&redirect_uri=${redirectUri}`;

  console.log("GitHub Auth URL:", githubAuthUrl); // Log para debug
  window.location.href = githubAuthUrl;
};
</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}
.github-button {
  padding: 10px 20px;
  background-color: #24292e;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
