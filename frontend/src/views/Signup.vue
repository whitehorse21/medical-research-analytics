<template>
  <div class="signup-container">
    <button @click="goBack" class="back-button" title="Go back">
      <span class="back-icon">←</span>
      <span class="back-text">Back</span>
    </button>
    <div class="signup-card">
      <h1>Medical Research Platform</h1>
      <h2>Sign Up</h2>
      <form @submit.prevent="handleSignup">
        <div v-if="error" class="error">{{ error }}</div>
        <div v-if="success" class="success">{{ success }}</div>
        <div class="form-group">
          <label>Username</label>
          <input
            v-model="username"
            type="text"
            required
            placeholder="Choose a username"
          />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="Enter your email (optional)"
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
        <div class="form-group">
          <label>Confirm Password</label>
          <input
            v-model="password2"
            type="password"
            required
            placeholder="Confirm your password"
          />
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? "Creating account..." : "Sign Up" }}
        </button>
        <p class="login-link">
          Already have an account?
          <router-link to="/login">Login</router-link>
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
const email = ref("");
const password = ref("");
const password2 = ref("");
const error = ref("");
const success = ref("");
const loading = ref(false);

const goBack = () => {
  router.push("/");
};

const handleSignup = async () => {
  error.value = "";
  success.value = "";
  loading.value = true;
  try {
    await auth.signup(username.value, email.value, password.value, password2.value);
    success.value = "Account created successfully! Redirecting to login...";
    setTimeout(() => {
      router.push("/login");
    }, 2000);
  } catch (err) {
    error.value = err.message || "Signup failed";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.signup-container {
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

@media (max-width: 768px) {
  .back-button {
    top: 1.5rem;
    left: 1.5rem;
    padding: 0.75rem 1.25rem;
    font-size: 0.9rem;
  }

  .back-icon {
    font-size: 1.25rem;
  }

  .back-text {
    font-size: 0.9rem;
  }
}

.signup-card {
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

.success {
  background: #efe;
  color: #3c3;
  padding: 0.75rem;
  border-radius: 5px;
  margin-bottom: 1rem;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
  color: #666;
}

.login-link a {
  color: #667eea;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
