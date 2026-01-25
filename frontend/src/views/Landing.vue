<template>
  <div class="min-h-screen bg-white dark:bg-gray-900 scroll-smooth transition-colors duration-300">
    <!-- Theme Toggle Button - Fixed in top right -->
    <button 
      @click="toggleTheme" 
      class="fixed top-4 right-4 z-[1000] flex items-center justify-center w-12 h-12 bg-white/15 dark:bg-white/10 backdrop-blur-xl text-white border-2 border-white/25 dark:border-white/20 rounded-xl cursor-pointer transition-all duration-300 hover:bg-white/25 dark:hover:bg-white/15 hover:border-white/40 dark:hover:border-white/30 hover:scale-110 active:scale-95 shadow-lg"
      :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    >
      <span class="text-2xl">{{ isDark ? '☀️' : '🌙' }}</span>
    </button>

    <!-- Hero Section -->
    <section ref="heroSection" class="relative h-screen min-h-screen flex items-center overflow-hidden bg-gradient-to-br from-indigo-500 to-purple-600">
      <div class="absolute inset-0 z-0">
        <div class="absolute inset-0 bg-gradient-to-br from-indigo-500/90 to-purple-600/90"></div>
        <img 
          src="https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=1920&q=80" 
          alt="Medical Research" 
          class="w-full h-full object-cover opacity-15 animate-zoom-in"
        />
      </div>
      <div class="relative z-10 max-w-[1400px] mx-auto px-8 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center w-full py-16 lg:py-0">
        <div class="text-white" :class="{ 'animate-in': heroAnimated }">
          <h1 class="text-5xl lg:text-7xl font-extrabold leading-tight mb-6 tracking-tight">
            <span class="block" :class="{ 'fade-in-up': heroAnimated }" style="animation-delay: 0.1s">
              Advanced Medical
            </span>
            <span class="block bg-gradient-to-r from-yellow-300 to-yellow-100 bg-clip-text text-transparent" :class="{ 'fade-in-up': heroAnimated }" style="animation-delay: 0.2s">
              Research Platform
            </span>
          </h1>
          <p class="text-xl lg:text-2xl leading-relaxed mb-10 opacity-95 max-w-[600px]" :class="{ 'fade-in-up': heroAnimated }" style="animation-delay: 0.3s">
            Streamline clinical studies, manage participants, and curate medical literature 
            in one comprehensive platform designed for researchers.
          </p>
          <div class="flex gap-4 flex-wrap" :class="{ 'fade-in-up': heroAnimated }" style="animation-delay: 0.4s">
            <router-link to="/signup" class="inline-flex items-center gap-2 px-8 py-4 rounded-xl text-base font-semibold no-underline transition-all duration-300 relative overflow-hidden bg-white text-indigo-600 shadow-lg hover:-translate-y-0.5 hover:shadow-xl btn-primary">
              <span class="relative z-10">Get Started</span>
              <span class="text-xl relative z-10 transition-transform duration-300">→</span>
            </router-link>
            <router-link to="/login" class="inline-flex items-center gap-2 px-8 py-4 rounded-xl text-base font-semibold no-underline transition-all duration-300 bg-white/20 text-white border-2 border-white/30 backdrop-blur-md hover:bg-white/30 hover:border-white/50">
              <span>Sign In</span>
            </router-link>
          </div>
        </div>
        <div class="relative" :class="{ 'fade-in-left': heroAnimated }" style="animation-delay: 0.5s">
          <img 
            src="https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=800&q=80" 
            alt="Medical Research Laboratory" 
            class="w-full h-auto rounded-3xl shadow-2xl border-4 border-white/20 transition-transform duration-300 hover:scale-[1.02]"
          />
        </div>
      </div>
      <div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-white text-sm opacity-80 z-20" :class="{ 'fade-in': heroAnimated }" style="animation-delay: 1s">
        <div class="w-6 h-10 border-2 border-white rounded-xl relative">
          <div class="absolute top-2 left-1/2 -translate-x-1/2 w-1 h-2 bg-white rounded-sm animate-scroll"></div>
        </div>
        <span>Scroll to explore</span>
      </div>
    </section>

    <!-- Features Section -->
    <section ref="featuresSection" class="py-24 bg-gradient-to-b from-gray-50 to-white dark:from-gray-800 dark:to-gray-900 relative overflow-hidden transition-colors duration-300">
      <div class="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-gray-200 dark:via-gray-700 to-transparent"></div>
      <div class="max-w-[1400px] mx-auto px-8 relative z-10">
        <div class="text-center mb-16" :class="{ 'fade-in-up': featuresAnimated }">
          <h2 class="text-4xl lg:text-5xl font-bold mb-4 bg-gradient-to-r from-indigo-500 to-purple-600 bg-clip-text text-transparent dark:text-gray-100">
            Powerful Features for Medical Research
          </h2>
          <p class="text-lg lg:text-xl text-gray-600 dark:text-gray-400">
            Everything you need to conduct, manage, and analyze clinical research
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div 
            v-for="(feature, index) in features" 
            :key="index"
            class="group bg-white dark:bg-gray-800 p-10 rounded-2xl shadow-sm dark:shadow-gray-900/50 transition-all duration-300 border border-gray-200 dark:border-gray-700 relative overflow-hidden hover:-translate-y-2 hover:shadow-xl dark:hover:shadow-gray-900 hover:border-indigo-500 dark:hover:border-indigo-400"
            :class="{ 'fade-in-up': featuresAnimated }"
            :style="`animation-delay: ${0.1 * index}s`"
          >
            <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 to-purple-600 scale-x-0 origin-left transition-transform duration-300 group-hover:scale-x-100"></div>
            <div class="text-5xl mb-6 block transition-transform duration-300 group-hover:scale-110 group-hover:rotate-[5deg]">{{ feature.icon }}</div>
            <h3 class="text-2xl font-semibold text-gray-900 dark:text-gray-100 mb-4">{{ feature.title }}</h3>
            <p class="text-base text-gray-600 dark:text-gray-400 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section ref="statsSection" class="py-12 md:py-16 bg-gradient-to-br from-indigo-500 to-purple-600 text-white relative overflow-hidden">
      <div class="absolute -top-1/2 -left-1/2 w-[200%] h-[200%] bg-[radial-gradient(circle,rgba(255,255,255,0.1)_1px,transparent_1px)] bg-[length:50px_50px] animate-move-pattern"></div>
      <div class="mx-auto px-4 sm:px-6 md:px-8">
        <div class="flex flex-col md:flex-row items-center justify-center gap-2 sm:gap-4 md:gap-8 lg:gap-12 text-center relative z-10">
          <div 
            v-for="(stat, index) in stats" 
            :key="index"
            class="p-2 sm:p-3 md:p-4 transition-transform duration-300 hover:scale-105"
            :class="{ 'fade-in-up': statsAnimated }"
            :style="`animation-delay: ${0.1 * index}s`"
          >
            <div class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-extrabold mb-1 sm:mb-2 bg-gradient-to-r from-yellow-300 to-yellow-100 bg-clip-text text-transparent" :class="{ 'count-up': statsAnimated }">
              {{ statAnimated ? stat.value : '0' }}
            </div>
            <div class="text-xs sm:text-sm md:text-base lg:text-lg opacity-90 font-medium">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section ref="ctaSection" class="py-24 bg-white dark:bg-gray-900 relative transition-colors duration-300">
      <div class="max-w-[1400px] mx-auto px-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center" :class="{ 'fade-in-up': ctaAnimated }">
          <div class="relative" :class="{ 'fade-in-left': ctaAnimated }">
            <img 
              src="https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=600&q=80" 
              alt="Research Team" 
              class="w-full h-auto rounded-3xl shadow-xl transition-transform duration-300 hover:scale-[1.02]"
            />
          </div>
          <div class="py-8" :class="{ 'fade-in-right': ctaAnimated }">
            <h2 class="text-4xl lg:text-5xl font-bold text-gray-900 dark:text-gray-100 mb-6 leading-tight">Ready to Transform Your Research?</h2>
            <p class="text-lg lg:text-xl text-gray-600 dark:text-gray-400 leading-relaxed mb-10">
              Join leading medical researchers who trust our platform to streamline 
              their clinical studies and accelerate medical discoveries.
            </p>
            <div class="flex gap-4 flex-wrap">
              <router-link to="/signup" class="inline-flex items-center gap-2 px-10 py-5 rounded-xl text-lg font-semibold no-underline transition-all duration-300 relative overflow-hidden bg-white text-indigo-600 shadow-lg hover:-translate-y-0.5 hover:shadow-xl btn-primary">
                <span class="relative z-10">Start Free Trial</span>
                <span class="text-xl relative z-10 transition-transform duration-300">→</span>
              </router-link>
              <router-link to="/login" class="inline-flex items-center gap-2 px-10 py-5 rounded-xl text-lg font-semibold no-underline transition-all duration-300 bg-transparent text-indigo-600 dark:text-indigo-400 border-2 border-indigo-600 dark:border-indigo-400 hover:bg-indigo-600 dark:hover:bg-indigo-400 hover:text-white">
                <span>Sign In to Account</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer ref="footerSection" class="bg-gray-900 text-white py-16 pt-16 pb-8 relative">
      <div class="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-gray-700 to-transparent"></div>
      <div class="max-w-[1400px] mx-auto px-8">
        <div class="grid grid-cols-1 lg:grid-cols-5 gap-16 mb-12" :class="{ 'fade-in-up': footerAnimated }">
          <div class="flex gap-4 items-start">
            <div class="text-4xl drop-shadow-lg">🔬</div>
            <div>
              <h3 class="text-xl font-semibold mb-2">Medical Research Platform</h3>
              <p class="text-gray-400 text-sm">Empowering medical research through technology</p>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 lg:col-span-4">
            <div>
              <h4 class="text-base font-semibold mb-4">Platform</h4>
              <div class="flex flex-col gap-3">
                <router-link to="/dashboard" class="text-gray-400 text-sm no-underline transition-all duration-200 relative pl-0 hover:text-white hover:pl-4 footer-link">Dashboard</router-link>
                <router-link to="/studies" class="text-gray-400 text-sm no-underline transition-all duration-200 relative pl-0 hover:text-white hover:pl-4 footer-link">Studies</router-link>
                <router-link to="/participants" class="text-gray-400 text-sm no-underline transition-all duration-200 relative pl-0 hover:text-white hover:pl-4 footer-link">Participants</router-link>
                <router-link to="/literature" class="text-gray-400 text-sm no-underline transition-all duration-200 relative pl-0 hover:text-white hover:pl-4 footer-link">Literature</router-link>
              </div>
            </div>
            <div>
              <h4 class="text-base font-semibold mb-4">Account</h4>
              <div class="flex flex-col gap-3">
                <router-link to="/login" class="text-gray-400 text-sm no-underline transition-all duration-200 relative pl-0 hover:text-white hover:pl-4 footer-link">Sign In</router-link>
                <router-link to="/signup" class="text-gray-400 text-sm no-underline transition-all duration-200 relative pl-0 hover:text-white hover:pl-4 footer-link">Sign Up</router-link>
              </div>
            </div>
            <div>
              <h4 class="text-base font-semibold mb-4">Support</h4>
              <div class="flex flex-col gap-3">
                <a href="#" class="text-gray-400 text-sm no-underline transition-all duration-200 relative pl-0 hover:text-white hover:pl-4 footer-link">Documentation</a>
                <a href="#" class="text-gray-400 text-sm no-underline transition-all duration-200 relative pl-0 hover:text-white hover:pl-4 footer-link">Contact</a>
                <a href="#" class="text-gray-400 text-sm no-underline transition-all duration-200 relative pl-0 hover:text-white hover:pl-4 footer-link">Privacy Policy</a>
              </div>
            </div>
          </div>
        </div>
        <div class="pt-8 border-t border-gray-800 text-center text-gray-400 text-sm" :class="{ 'fade-in': footerAnimated }">
          <p>&copy; 2024 Medical Research Platform. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useTheme } from "../composables/useTheme";

const { isDark, toggleTheme } = useTheme();

const heroSection = ref(null);
const featuresSection = ref(null);
const statsSection = ref(null);
const ctaSection = ref(null);
const footerSection = ref(null);

const heroAnimated = ref(false);
const featuresAnimated = ref(false);
const statsAnimated = ref(false);
const ctaAnimated = ref(false);
const footerAnimated = ref(false);
const statAnimated = ref(false);

const features = [
  {
    icon: "📊",
    title: "Clinical Studies Management",
    description: "Create, track, and manage clinical studies with comprehensive status tracking, date management, and participant enrollment."
  },
  {
    icon: "👥",
    title: "Participant Tracking",
    description: "Efficiently manage participant enrollment, demographics, and enrollment dates with detailed analytics and reporting."
  },
  {
    icon: "📚",
    title: "Literature Repository",
    description: "Build and maintain a comprehensive library of medical literature with DOI tracking, abstracts, and publication metadata."
  },
  {
    icon: "📈",
    title: "Analytics Dashboard",
    description: "Real-time insights into your research with comprehensive statistics, completion rates, demographics, and publication trends."
  },
  {
    icon: "🔒",
    title: "Secure & Compliant",
    description: "Built with security and compliance in mind, ensuring your research data is protected and meets regulatory requirements."
  },
  {
    icon: "⚡",
    title: "Fast & Reliable",
    description: "Modern, responsive interface that works seamlessly across all devices with real-time updates and instant data access."
  }
];

const stats = [
  { value: "100%", label: "Secure" },
  { value: "24/7", label: "Available" },
  { value: "99.9%", label: "Uptime" },
  { value: "HIPAA", label: "Compliant" }
];

let observer = null;

const setupIntersectionObserver = () => {
  const options = {
    root: null,
    rootMargin: "0px",
    threshold: 0.2
  };

  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        if (entry.target === heroSection.value) {
          heroAnimated.value = true;
        } else if (entry.target === featuresSection.value) {
          featuresAnimated.value = true;
        } else if (entry.target === statsSection.value) {
          statsAnimated.value = true;
          statAnimated.value = true;
        } else if (entry.target === ctaSection.value) {
          ctaAnimated.value = true;
        } else if (entry.target === footerSection.value) {
          footerAnimated.value = true;
        }
      }
    });
  }, options);

  // Observe all sections
  if (heroSection.value) observer.observe(heroSection.value);
  if (featuresSection.value) observer.observe(featuresSection.value);
  if (statsSection.value) observer.observe(statsSection.value);
  if (ctaSection.value) observer.observe(ctaSection.value);
  if (footerSection.value) observer.observe(footerSection.value);
};

onMounted(() => {
  // Trigger hero animation immediately
  heroAnimated.value = true;
  
  // Setup intersection observer for other sections
  setupIntersectionObserver();
});

onUnmounted(() => {
  if (observer) {
    observer.disconnect();
  }
});
</script>

<style scoped>
/* Custom keyframes - required for animations */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes countUp {
  from {
    opacity: 0;
    transform: scale(0.5);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes zoomIn {
  from {
    transform: scale(1);
  }
  to {
    transform: scale(1.1);
  }
}

@keyframes scroll {
  0% {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  100% {
    opacity: 0;
    transform: translateX(-50%) translateY(12px);
  }
}

@keyframes movePattern {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(50px, 50px);
  }
}

/* Animation classes */
.fade-in-up {
  opacity: 0;
  animation: fadeInUp 0.8s ease-out forwards;
}

.fade-in-left {
  opacity: 0;
  animation: fadeInLeft 0.8s ease-out forwards;
}

.fade-in-right {
  opacity: 0;
  animation: fadeInRight 0.8s ease-out forwards;
}

.fade-in {
  opacity: 0;
  animation: fadeIn 0.8s ease-out forwards;
}

.count-up {
  animation: countUp 0.6s ease-out forwards;
}

.animate-zoom-in {
  animation: zoomIn 20s ease-in-out infinite alternate;
}

.animate-scroll {
  animation: scroll 1.5s infinite;
}

.animate-move-pattern {
  animation: movePattern 20s linear infinite;
}

/* Button ripple effect - requires pseudo-element (can't be done with Tailwind alone) */
.btn-primary::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.btn-primary:hover::before {
  width: 300px;
  height: 300px;
}

/* Footer link arrow - requires pseudo-element with content (can't be done with Tailwind alone) */
.footer-link::before {
  content: '→';
  position: absolute;
  left: -1rem;
  opacity: 0;
  transition: all 0.2s;
}

.footer-link:hover::before {
  opacity: 1;
  left: 0;
}
</style>
