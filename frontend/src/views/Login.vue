<template>
  <div class="min-h-screen h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 relative overflow-x-hidden w-full box-border p-4 md:p-4 sm:p-4 sm:py-8">
    <button 
      @click="goBack" 
      class="absolute top-4 left-4 flex items-center gap-2 bg-white/15 text-white border-2 border-white/25 px-4 py-2.5 rounded-xl cursor-pointer text-sm font-semibold transition-all duration-300 backdrop-blur-xl z-10 shadow-lg overflow-hidden hover:bg-white/25 hover:border-white/40 hover:-translate-x-1 hover:shadow-xl active:scale-95 sm:top-3 sm:left-3 sm:px-3 sm:py-2 sm:text-xs"
      title="Go back"
    >
      <span class="text-xl leading-none relative z-[1] sm:text-base">←</span>
      <span class="text-sm relative z-[1] tracking-wide sm:hidden">Back</span>
    </button>
    <div class="bg-white p-8 rounded-2xl shadow-2xl w-full max-w-[400px] lg:max-w-[450px] md:p-6 md:max-w-[90%] sm:p-6 sm:max-w-[95%] sm:rounded-3xl border-4 border-indigo-200 relative overflow-hidden">
      <!-- Decorative gradient overlay for Login -->
      <div class="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-indigo-400 via-purple-400 to-indigo-400"></div>
      <div class="relative">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg sm:w-10 sm:h-10">
            <span class="text-2xl sm:text-xl">🔐</span>
          </div>
          <div>
            <h1 class="m-0 text-gray-800 text-xl font-bold sm:text-lg">Medical Research</h1>
            <p class="m-0 text-gray-500 text-xs sm:text-xs">Platform</p>
          </div>
        </div>
        <h2 class="m-0 mb-6 text-indigo-600 text-2xl font-bold md:text-xl sm:text-lg">Welcome Back</h2>
      <form @submit.prevent="handleLogin">
        <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-md mb-4">{{ error }}</div>
        <div class="mb-4">
          <label class="block mb-2 text-gray-800 font-medium">Username</label>
          <input
            v-model="username"
            type="text"
            required
            placeholder="Enter your username"
            class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-base box-border focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all sm:text-base sm:px-3"
          />
        </div>
        <div class="mb-4">
          <label class="block mb-2 text-gray-800 font-medium">Password</label>
          <input
            v-model="password"
            type="password"
            required
            placeholder="Enter your password"
            class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl text-base box-border focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all sm:text-base sm:px-3"
          />
        </div>
        <button 
          type="submit" 
          :disabled="loading"
          class="w-full px-3 py-3.5 bg-gradient-to-r from-indigo-500 to-purple-600 text-white border-0 rounded-xl text-base font-semibold cursor-pointer mt-4 hover:from-indigo-600 hover:to-purple-700 disabled:opacity-60 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-xl hover:scale-[1.02] active:scale-[0.98] sm:py-3"
        >
          {{ loading ? "Logging in..." : "Login" }}
        </button>
        <p class="text-center mt-4 text-gray-600">
          Don't have an account?
          <router-link to="/signup" class="text-indigo-600 font-semibold no-underline hover:underline hover:text-purple-600 transition-colors">Sign up</router-link>
        </p>
      </form>
      </div>
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
