import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", () => {
  const token = useState("auth_token", () => null);
  const user = useState("auth_user", () => null);

  const isAuthenticated = computed(() => !!token.value);

  function setToken(newToken) {
    token.value = newToken;
    if (import.meta.client) {
      localStorage.setItem("github_token", newToken);
    }
  }

  function setUser(newUser) {
    user.value = newUser;
    if (import.meta.client) {
      localStorage.setItem("github_user", JSON.stringify(newUser));
    }
  }

  function logout() {
    token.value = null;
    user.value = null;
    if (import.meta.client) {
      localStorage.removeItem("github_token");
      localStorage.removeItem("github_user");
    }
  }

  function initializeFromStorage() {
    if (import.meta.client) {
      const storedToken = localStorage.getItem("github_token");
      const storedUser = JSON.parse(
        localStorage.getItem("github_user") || "null"
      );
      if (storedToken) token.value = storedToken;
      if (storedUser) user.value = storedUser;
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    setToken,
    setUser,
    logout,
    initializeFromStorage,
  };
});
