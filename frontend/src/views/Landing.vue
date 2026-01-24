<template>
  <div class="landing-page">
    <!-- Hero Section -->
    <section class="hero" ref="heroSection">
      <div class="hero-background">
        <div class="hero-overlay"></div>
        <img 
          src="https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=1920&q=80" 
          alt="Medical Research" 
          class="hero-image"
        />
      </div>
      <div class="hero-content">
        <div class="hero-text" :class="{ 'animate-in': heroAnimated }">
          <h1 class="hero-title">
            <span class="title-line" :class="{ 'fade-in-up': heroAnimated }" style="animation-delay: 0.1s">
              Advanced Medical
            </span>
            <span class="title-line highlight" :class="{ 'fade-in-up': heroAnimated }" style="animation-delay: 0.2s">
              Research Platform
            </span>
          </h1>
          <p class="hero-subtitle" :class="{ 'fade-in-up': heroAnimated }" style="animation-delay: 0.3s">
            Streamline clinical studies, manage participants, and curate medical literature 
            in one comprehensive platform designed for researchers.
          </p>
          <div class="hero-actions" :class="{ 'fade-in-up': heroAnimated }" style="animation-delay: 0.4s">
            <router-link to="/signup" class="btn btn-primary">
              <span>Get Started</span>
              <span class="btn-icon">→</span>
            </router-link>
            <router-link to="/login" class="btn btn-secondary">
              <span>Sign In</span>
            </router-link>
          </div>
        </div>
        <div class="hero-image-container" :class="{ 'fade-in-left': heroAnimated }" style="animation-delay: 0.5s">
          <img 
            src="https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=800&q=80" 
            alt="Medical Research Laboratory" 
            class="hero-main-image"
          />
        </div>
      </div>
      <div class="scroll-indicator" :class="{ 'fade-in': heroAnimated }" style="animation-delay: 1s">
        <div class="mouse">
          <div class="wheel"></div>
        </div>
        <span>Scroll to explore</span>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features" ref="featuresSection">
      <div class="container">
        <div class="section-header" :class="{ 'fade-in-up': featuresAnimated }">
          <h2 class="section-title">Powerful Features for Medical Research</h2>
          <p class="section-subtitle">
            Everything you need to conduct, manage, and analyze clinical research
          </p>
        </div>
        <div class="features-grid">
          <div 
            v-for="(feature, index) in features" 
            :key="index"
            class="feature-card"
            :class="{ 'fade-in-up': featuresAnimated }"
            :style="`animation-delay: ${0.1 * index}s`"
          >
            <div class="feature-icon">{{ feature.icon }}</div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="stats" ref="statsSection">
      <div class="container">
        <div class="stats-grid">
          <div 
            v-for="(stat, index) in stats" 
            :key="index"
            class="stat-item"
            :class="{ 'fade-in-up': statsAnimated }"
            :style="`animation-delay: ${0.1 * index}s`"
          >
            <div class="stat-number" :class="{ 'count-up': statsAnimated }">{{ statAnimated ? stat.value : '0' }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta" ref="ctaSection">
      <div class="container">
        <div class="cta-content" :class="{ 'fade-in-up': ctaAnimated }">
          <div class="cta-image-wrapper" :class="{ 'fade-in-left': ctaAnimated }">
            <img 
              src="https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=600&q=80" 
              alt="Research Team" 
              class="cta-image"
            />
          </div>
          <div class="cta-text" :class="{ 'fade-in-right': ctaAnimated }">
            <h2 class="cta-title">Ready to Transform Your Research?</h2>
            <p class="cta-description">
              Join leading medical researchers who trust our platform to streamline 
              their clinical studies and accelerate medical discoveries.
            </p>
            <div class="cta-actions">
              <router-link to="/signup" class="btn btn-primary large">
                <span>Start Free Trial</span>
                <span class="btn-icon">→</span>
              </router-link>
              <router-link to="/login" class="btn btn-outline large">
                <span>Sign In to Account</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer" ref="footerSection">
      <div class="container">
        <div class="footer-content" :class="{ 'fade-in-up': footerAnimated }">
          <div class="footer-brand">
            <div class="footer-logo">🔬</div>
            <div class="footer-text">
              <h3>Medical Research Platform</h3>
              <p>Empowering medical research through technology</p>
            </div>
          </div>
          <div class="footer-links">
            <div class="footer-column">
              <h4>Platform</h4>
              <router-link to="/dashboard">Dashboard</router-link>
              <router-link to="/studies">Studies</router-link>
              <router-link to="/participants">Participants</router-link>
              <router-link to="/literature">Literature</router-link>
            </div>
            <div class="footer-column">
              <h4>Account</h4>
              <router-link to="/login">Sign In</router-link>
              <router-link to="/signup">Sign Up</router-link>
            </div>
            <div class="footer-column">
              <h4>Support</h4>
              <a href="#">Documentation</a>
              <a href="#">Contact</a>
              <a href="#">Privacy Policy</a>
            </div>
          </div>
        </div>
        <div class="footer-bottom" :class="{ 'fade-in': footerAnimated }">
          <p>&copy; 2024 Medical Research Platform. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

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
.landing-page {
  min-height: 100vh;
  background: #ffffff;
  scroll-behavior: smooth;
}

/* Animation Classes */
.fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
  opacity: 0;
}

.fade-in-left {
  animation: fadeInLeft 0.8s ease-out forwards;
  opacity: 0;
}

.fade-in-right {
  animation: fadeInRight 0.8s ease-out forwards;
  opacity: 0;
}

.fade-in {
  animation: fadeIn 0.8s ease-out forwards;
  opacity: 0;
}

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

.count-up {
  animation: countUp 0.6s ease-out forwards;
}

/* Hero Section */
.hero {
  position: relative;
  height: 100vh;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.15;
  animation: zoomIn 20s ease-in-out infinite alternate;
}

@keyframes zoomIn {
  from {
    transform: scale(1);
  }
  to {
    transform: scale(1.1);
  }
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 1400px;
  margin: 0 auto;
  padding: 4rem 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  width: 100%;
}

.hero-text {
  color: white;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  margin: 0 0 1.5rem 0;
  letter-spacing: -1px;
}

.title-line {
  display: block;
}

.title-line.highlight {
  background: linear-gradient(120deg, #ffd700 0%, #ffed4e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  margin: 0 0 2.5rem 0;
  opacity: 0.95;
  max-width: 600px;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.hero-image-container {
  position: relative;
}

.hero-main-image {
  width: 100%;
  height: auto;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 4px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s ease;
}

.hero-main-image:hover {
  transform: scale(1.02);
}

.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  color: white;
  font-size: 0.875rem;
  opacity: 0.8;
  z-index: 2;
}

.mouse {
  width: 24px;
  height: 40px;
  border: 2px solid white;
  border-radius: 12px;
  position: relative;
}

.wheel {
  width: 4px;
  height: 8px;
  background: white;
  border-radius: 2px;
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
  animation: scroll 1.5s infinite;
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

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  cursor: pointer;
  white-space: nowrap;
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.btn:hover::before {
  width: 300px;
  height: 300px;
}

.btn-primary {
  background: white;
  color: #667eea;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-outline {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-outline:hover {
  background: #667eea;
  color: white;
}

.btn.large {
  padding: 1.25rem 2.5rem;
  font-size: 1.125rem;
}

.btn-icon {
  font-size: 1.25rem;
  transition: transform 0.3s;
  position: relative;
  z-index: 1;
}

.btn:hover .btn-icon {
  transform: translateX(4px);
}

.btn span {
  position: relative;
  z-index: 1;
}

/* Features Section */
.features {
  padding: 6rem 0;
  background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);
  position: relative;
  overflow: hidden;
}

.features::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 1;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-subtitle {
  font-size: 1.125rem;
  color: #718096;
  margin: 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #e2e8f0;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s;
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  display: block;
  transition: transform 0.3s;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1) rotate(5deg);
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 1rem 0;
}

.feature-description {
  font-size: 1rem;
  color: #718096;
  line-height: 1.6;
  margin: 0;
}

/* Stats Section */
.stats {
  padding: 4rem 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.stats::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: movePattern 20s linear infinite;
}

@keyframes movePattern {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(50px, 50px);
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 3rem;
  text-align: center;
  position: relative;
  z-index: 1;
}

.stat-item {
  padding: 1rem;
  transition: transform 0.3s;
}

.stat-item:hover {
  transform: scale(1.05);
}

.stat-number {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  background: linear-gradient(120deg, #ffd700 0%, #ffed4e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 1.125rem;
  opacity: 0.9;
  font-weight: 500;
}

/* CTA Section */
.cta {
  padding: 6rem 0;
  background: white;
  position: relative;
}

.cta-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.cta-image-wrapper {
  position: relative;
}

.cta-image {
  width: 100%;
  height: auto;
  border-radius: 20px;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.cta-image-wrapper:hover .cta-image {
  transform: scale(1.02);
}

.cta-text {
  padding: 2rem 0;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 1.5rem 0;
  line-height: 1.2;
}

.cta-description {
  font-size: 1.125rem;
  color: #718096;
  line-height: 1.6;
  margin: 0 0 2.5rem 0;
}

.cta-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

/* Footer */
.footer {
  background: #1a202c;
  color: white;
  padding: 4rem 0 2rem;
  position: relative;
}

.footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, #2d3748, transparent);
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 3fr;
  gap: 4rem;
  margin-bottom: 3rem;
}

.footer-brand {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.footer-logo {
  font-size: 2.5rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.footer-text h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.footer-text p {
  margin: 0;
  color: #a0aec0;
  font-size: 0.875rem;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.footer-column h4 {
  margin: 0 0 1rem 0;
  font-size: 1rem;
  font-weight: 600;
  color: white;
}

.footer-column a {
  display: block;
  color: #a0aec0;
  text-decoration: none;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  transition: all 0.2s;
  position: relative;
  padding-left: 0;
}

.footer-column a::before {
  content: '→';
  position: absolute;
  left: -1rem;
  opacity: 0;
  transition: all 0.2s;
}

.footer-column a:hover {
  color: white;
  padding-left: 1rem;
}

.footer-column a:hover::before {
  opacity: 1;
  left: 0;
}

.footer-bottom {
  padding-top: 2rem;
  border-top: 1px solid #2d3748;
  text-align: center;
  color: #a0aec0;
  font-size: 0.875rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .cta-content {
    grid-template-columns: 1fr;
  }

  .footer-content {
    grid-template-columns: 1fr;
  }

  .footer-links {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero {
    height: 100vh;
    min-height: 100vh;
  }

  .hero-content {
    padding: 2rem 1rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
  }

  .cta-title {
    font-size: 2rem;
  }

  .footer-links {
    grid-template-columns: 1fr;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }

  .hero-actions,
  .cta-actions {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 1.75rem;
  }

  .stat-number {
    font-size: 2rem;
  }

  .feature-card {
    padding: 1.5rem;
  }
}
</style>
