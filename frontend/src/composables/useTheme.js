import { ref } from 'vue';

// Create a shared reactive state
const isDark = ref(false);

// Apply theme to document
const applyTheme = (dark) => {
  if (typeof document === 'undefined') return;
  
  const html = document.documentElement;
  // Remove dark class first to ensure clean state
  html.classList.remove('dark');
  
  if (dark) {
    html.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  } else {
    html.classList.remove('dark');
    localStorage.setItem('theme', 'light');
  }
  
  // Force a reflow to ensure the class is applied
  void html.offsetHeight;
};

// Initialize theme from localStorage or system preference
const initTheme = () => {
  if (typeof window === 'undefined' || typeof document === 'undefined') return;
  
  const savedTheme = localStorage.getItem('theme');
  let shouldBeDark = false;
  
  if (savedTheme) {
    shouldBeDark = savedTheme === 'dark';
  } else {
    // Check system preference
    shouldBeDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  
  isDark.value = shouldBeDark;
  applyTheme(shouldBeDark);
};

// Watch for system theme changes
let mediaQueryListener = null;
const watchSystemTheme = () => {
  if (typeof window === 'undefined') return;
  
  // Remove existing listener if any
  if (mediaQueryListener) {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.removeEventListener('change', mediaQueryListener);
  }
  
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  mediaQueryListener = (e) => {
    // Only auto-apply if user hasn't manually set a preference
    if (!localStorage.getItem('theme')) {
      isDark.value = e.matches;
      applyTheme(e.matches);
    }
  };
  mediaQuery.addEventListener('change', mediaQueryListener);
};

// Initialize immediately when module loads
if (typeof window !== 'undefined' && typeof document !== 'undefined') {
  // Run immediately
  initTheme();
  watchSystemTheme();
}

export function useTheme() {
  // Toggle theme
  const toggleTheme = () => {
    const newValue = !isDark.value;
    isDark.value = newValue;
    // Force apply immediately
    applyTheme(newValue);
    // Also trigger a small delay to ensure it's applied
    if (typeof window !== 'undefined') {
      setTimeout(() => {
        applyTheme(newValue);
      }, 0);
    }
  };

  return {
    isDark,
    toggleTheme,
    initTheme,
  };
}
