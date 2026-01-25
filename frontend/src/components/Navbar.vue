<template>
  <nav class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg sticky top-0 z-[1000] backdrop-blur-sm py-2">
    <div class="max-w-[1400px] mx-auto px-8 flex items-center justify-between gap-8 h-[70px] lg:px-6 lg:gap-4 md:px-4 md:h-[60px] sm:h-[56px]">
      <div class="flex-shrink-0">
        <router-link to="/dashboard" class="flex items-center gap-3 text-white no-underline transition-opacity hover:opacity-90">
          <div class="text-3xl leading-none drop-shadow-md md:text-2xl sm:text-xl">🔬</div>
          <div class="flex flex-col leading-tight">
            <span class="text-xl font-bold tracking-tight md:text-base sm:text-sm">Medical Research</span>
            <span class="text-xs opacity-90 font-normal tracking-wide xl:hidden">Clinical Data Platform</span>
          </div>
        </router-link>
      </div>
      
      <button 
        @click="toggleMobileMenu" 
        class="md:hidden flex flex-col justify-around w-8 h-8 bg-transparent border-0 cursor-pointer p-0 z-100 gap-1"
        :aria-label="mobileMenuOpen ? 'Close menu' : 'Open menu'"
      >
        <span 
          class="w-full h-[3px] bg-white rounded-sm transition-all duration-300 origin-center"
          :class="mobileMenuOpen ? 'rotate-45 translate-x-1.5 translate-y-1.5' : ''"
        ></span>
        <span 
          class="w-full h-[3px] bg-white rounded-sm transition-all duration-300 origin-center"
          :class="mobileMenuOpen ? 'opacity-0' : ''"
        ></span>
        <span 
          class="w-full h-[3px] bg-white rounded-sm transition-all duration-300 origin-center"
          :class="mobileMenuOpen ? '-rotate-45 translate-x-1.5 -translate-y-1.5' : ''"
        ></span>
      </button>

      <!-- Desktop Navigation (visible on lg and above) -->
      <div class="hidden md:flex items-center gap-2 flex-1 justify-center">
        <router-link 
          to="/dashboard" 
          class="flex items-center gap-2 px-5 py-3 text-white/90 no-underline rounded-lg font-medium text-[0.9375rem] transition-all whitespace-nowrap relative hover:bg-white/15 hover:text-white hover:-translate-y-px"
          active-class="bg-white/25 text-white font-semibold shadow-md after:content-[''] after:absolute after:bottom-0 after:left-1/2 after:-translate-x-1/2 after:w-[60%] after:h-[3px] after:bg-white after:rounded-t-sm"
        >
          <span class="text-lg leading-none">📊</span>
          <span class="text-[0.9375rem] xl:inline hidden">Dashboard</span>
        </router-link>
        <router-link 
          to="/studies" 
          class="flex items-center gap-2 px-5 py-3 text-white/90 no-underline rounded-lg font-medium text-[0.9375rem] transition-all whitespace-nowrap relative hover:bg-white/15 hover:text-white hover:-translate-y-px"
          active-class="bg-white/25 text-white font-semibold shadow-md after:content-[''] after:absolute after:bottom-0 after:left-1/2 after:-translate-x-1/2 after:w-[60%] after:h-[3px] after:bg-white after:rounded-t-sm"
        >
          <span class="text-lg leading-none">📋</span>
          <span class="text-[0.9375rem] xl:inline hidden">Studies</span>
        </router-link>
        <router-link 
          to="/participants" 
          class="flex items-center gap-2 px-5 py-3 text-white/90 no-underline rounded-lg font-medium text-[0.9375rem] transition-all whitespace-nowrap relative hover:bg-white/15 hover:text-white hover:-translate-y-px"
          active-class="bg-white/25 text-white font-semibold shadow-md after:content-[''] after:absolute after:bottom-0 after:left-1/2 after:-translate-x-1/2 after:w-[60%] after:h-[3px] after:bg-white after:rounded-t-sm"
        >
          <span class="text-lg leading-none">👥</span>
          <span class="text-[0.9375rem] xl:inline hidden">Participants</span>
        </router-link>
        <router-link 
          to="/literature" 
          class="flex items-center gap-2 px-5 py-3 text-white/90 no-underline rounded-lg font-medium text-[0.9375rem] transition-all whitespace-nowrap relative hover:bg-white/15 hover:text-white hover:-translate-y-px"
          active-class="bg-white/25 text-white font-semibold shadow-md after:content-[''] after:absolute after:bottom-0 after:left-1/2 after:-translate-x-1/2 after:w-[60%] after:h-[3px] after:bg-white after:rounded-t-sm"
        >
          <span class="text-lg leading-none">📚</span>
          <span class="text-[0.9375rem] xl:inline hidden">Literature</span>
        </router-link>
      </div>

      <!-- Desktop User Section (visible on lg and above) -->
      <div class="hidden md:flex items-center gap-4 flex-shrink-0">
        <button 
          @click="toggleTheme" 
          class="flex items-center justify-center w-10 h-10 bg-white/15 rounded-xl transition-all hover:bg-white/20 text-white border border-white/20"
          :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
        >
          <span class="text-xl">{{ isDark ? '☀️' : '🌙' }}</span>
        </button>
        <div class="flex items-center gap-3 px-4 py-2 bg-white/15 rounded-xl transition-all hover:bg-white/20">
          <div class="w-10 h-10 rounded-full bg-white/30 flex items-center justify-center font-bold text-sm text-white border-2 border-white/30 shadow-md">
            <span>{{ getUserInitials() }}</span>
          </div>
          <div class="flex flex-col gap-0.5 xl:flex hidden">
            <span class="text-sm font-semibold text-white leading-tight">{{ currentUser?.username || 'User' }}</span>
            <span class="text-xs text-white/80 leading-tight">Researcher</span>
          </div>
        </div>
        <button 
          @click="handleLogout" 
          class="flex items-center gap-2 bg-white/20 text-white border border-white/30 px-5 py-2.5 rounded-lg cursor-pointer text-sm font-semibold transition-all whitespace-nowrap hover:bg-white/30 hover:border-white/50 hover:-translate-y-px hover:shadow-md"
          title="Logout"
        >
          <span class="text-base leading-none">🚪</span>
          <span class="text-sm xl:inline hidden">Logout</span>
        </button>
      </div>

      <!-- Mobile Navigation Drawer (visible on screens smaller than lg) -->
      <div 
        class="lg:hidden fixed top-18 left-0 right-0 bg-gradient-to-r from-indigo-500 to-purple-600 flex-col p-4 gap-2 transform -translate-x-full transition-transform duration-300 shadow-lg z-[999] max-h-[calc(100vh-60px)] overflow-y-auto md:top-[56px]"
        :class="{ 'translate-x-0': mobileMenuOpen }"
        @click="closeMobileMenu"
      >
        <router-link 
          to="/dashboard" 
          class="flex items-center gap-2 px-4 py-4 text-white/90 no-underline rounded-lg font-medium text-[0.9375rem] transition-all justify-start w-full hover:bg-white/15 hover:text-white"
          active-class="bg-white/25 text-white font-semibold"
        >
          <span class="text-xl leading-none">📊</span>
          <span class="text-[0.9375rem]">Dashboard</span>
        </router-link>
        <router-link 
          to="/studies" 
          class="flex items-center gap-2 px-4 py-4 text-white/90 no-underline rounded-lg font-medium text-[0.9375rem] transition-all justify-start w-full hover:bg-white/15 hover:text-white"
          active-class="bg-white/25 text-white font-semibold"
        >
          <span class="text-xl leading-none">📋</span>
          <span class="text-[0.9375rem]">Studies</span>
        </router-link>
        <router-link 
          to="/participants" 
          class="flex items-center gap-2 px-4 py-4 text-white/90 no-underline rounded-lg font-medium text-[0.9375rem] transition-all justify-start w-full hover:bg-white/15 hover:text-white"
          active-class="bg-white/25 text-white font-semibold"
        >
          <span class="text-xl leading-none">👥</span>
          <span class="text-[0.9375rem]">Participants</span>
        </router-link>
        <router-link 
          to="/literature" 
          class="flex items-center gap-2 px-4 py-4 text-white/90 no-underline rounded-lg font-medium text-[0.9375rem] transition-all justify-start w-full hover:bg-white/15 hover:text-white"
          active-class="bg-white/25 text-white font-semibold"
        >
          <span class="text-xl leading-none">📚</span>
          <span class="text-[0.9375rem]">Literature</span>
        </router-link>
      </div>

      <!-- Mobile User Section (visible on screens smaller than lg) -->
      <div 
        class="md:hidden fixed flex bottom-0 left-0 right-0 bg-gradient-to-r from-indigo-500 to-purple-600 p-4 flex-col gap-4 transform translate-y-full transition-transform duration-300 shadow-lg z-100 border-t border-white/20"
        :class="{ 'translate-y-0': mobileMenuOpen }"
      >
        <button 
          @click="toggleTheme" 
          class="flex items-center justify-center gap-2 bg-white/15 text-white border border-white/20 px-5 py-2.5 rounded-lg cursor-pointer text-sm font-semibold transition-all w-full hover:bg-white/20"
          :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
        >
          <span class="text-xl">{{ isDark ? '☀️' : '🌙' }}</span>
          <span class="text-sm">{{ isDark ? 'Light Mode' : 'Dark Mode' }}</span>
        </button>
        <div class="flex items-center gap-3 px-3 py-3 bg-white/15 rounded-xl w-full justify-center">
          <div class="w-10 h-10 rounded-full bg-white/30 flex items-center justify-center font-bold text-sm text-white border-2 border-white/30 shadow-md">
            <span>{{ getUserInitials() }}</span>
          </div>
          <div class="flex flex-col gap-0.5">
            <span class="text-sm font-semibold text-white leading-tight">{{ currentUser?.username || 'User' }}</span>
            <span class="text-xs text-white/80 leading-tight">Researcher</span>
          </div>
        </div>
        <button 
          @click="handleLogout" 
          class="flex items-center gap-2 bg-white/20 text-white border border-white/30 px-5 py-2.5 rounded-lg cursor-pointer text-sm font-semibold transition-all w-full justify-center hover:bg-white/30 hover:border-white/50"
          title="Logout"
        >
          <span class="text-base leading-none">🚪</span>
          <span class="text-sm">Logout</span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import { auth } from "../utils/api";
import { useTheme } from "../composables/useTheme";

const router = useRouter();
const currentUser = computed(() => auth.getCurrentUser());
const mobileMenuOpen = ref(false);
const { isDark, toggleTheme } = useTheme();

const getUserInitials = () => {
  if (!currentUser.value?.username) return "U";
  return currentUser.value.username
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .substring(0, 2);
};

const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

const closeMobileMenu = () => {
  mobileMenuOpen.value = false;
};

const handleLogout = async () => {
  await auth.logout();
  router.push("/login");
};
</script>
