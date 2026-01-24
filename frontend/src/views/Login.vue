<template>
  <div class="login-container">
    <button @click="goBack" class="back-button" title="Go back">
      <span class="back-icon">←</span>
      <span class="back-text">Back</span>
    </button>
    <div class="login-card">
      <h1>Medical Research Platform</h1>
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div v-if="error" class="error">{{ error }}</div>
        <div class="form-group">
          <label>Username</label>
          <input
            v-model="username"
            type="text"
            required
            placeholder="Enter your username"
          />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="Enter your password"
          />
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? "Logging in..." : "Login" }}
        </button>
        <p class="signup-link">
          Don't have an account?
          <router-link to="/signup">Sign up</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { auth } from "../utils/api";

const router = useRouter();
const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

const goBack = () => {
  router.push("/");
};

const handleLogin = async () => {
  error.value = "";
  loading.value = true;
  try {
    await auth.login(username.value, password.value);
    router.push("/dashboard");
  } catch (err) {
    error.value = err.message || "Login failed";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
}

.back-button {
  position: absolute;
  top: 2rem;
  left: 2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.25);
  padding: 0.875rem 1.75rem;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  backdrop-filter: blur(12px);
  z-index: 10;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  width: auto;
}

.back-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.back-button:hover::before {
  left: 100%;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateX(-6px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.back-button:active {
  transform: translateX(-4px) scale(0.98);
}

.back-icon {
  font-size: 1.5rem;
  line-height: 1;
  transition: transform 0.3s;
  position: relative;
  z-index: 1;
}

.back-button:hover .back-icon {
  transform: translateX(-3px);
}

.back-text {
  font-size: 1rem;
  position: relative;
  z-index: 1;
  letter-spacing: 0.3px;
}

@media (max-width: 1024px) {
  .login-card {
    max-width: 450px;
  }
}

@media (max-width: 768px) {
  .login-container {
    padding: 1rem;
  }

  .back-button {
    top: 1rem;
    left: 1rem;
    padding: 0.625rem 1rem;
    font-size: 0.875rem;
  }

  .back-icon {
    font-size: 1.125rem;
  }

  .back-text {
    font-size: 0.875rem;
  }

  .login-card {
    padding: 1.5rem;
    max-width: 100%;
  }

  h1 {
    font-size: 1.375rem;
  }

  h2 {
    font-size: 1.125rem;
  }
}

@media (max-width: 480px) {
  .login-container {
    padding: 0.75rem;
    align-items: flex-start;
    padding-top: 4rem;
  }

  .back-button {
    top: 0.75rem;
    left: 0.75rem;
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }

  .login-card {
    padding: 1.25rem;
  }

  h1 {
    font-size: 1.25rem;
  }

  h2 {
    font-size: 1rem;
  }

  input {
    font-size: 16px; /* Prevents zoom on iOS */
  }
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
}

h1 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.5rem;
}

h2 {
  margin: 0 0 1.5rem 0;
  color: #666;
  font-size: 1.2rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #667eea;
}

button {
  width: 100%;
  padding: 0.75rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
}

button:hover:not(:disabled) {
  background: #5568d3;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  background: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 5px;
  margin-bottom: 1rem;
}

.signup-link {
  text-align: center;
  margin-top: 1rem;
  color: #666;
}

.signup-link a {
  color: #667eea;
  text-decoration: none;
}

.signup-link a:hover {
  text-decoration: underline;
}
</style>
