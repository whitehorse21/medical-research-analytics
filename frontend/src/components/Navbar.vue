<template>
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-brand">
        <router-link to="/dashboard" class="brand-link">
          <div class="brand-icon">🔬</div>
          <div class="brand-text">
            <span class="brand-name">Medical Research</span>
            <span class="brand-tagline">Clinical Data Platform</span>
          </div>
        </router-link>
      </div>
      
      <div class="nav-menu">
        <router-link to="/dashboard" class="nav-link" active-class="active">
          <span class="nav-icon">📊</span>
          <span class="nav-text">Dashboard</span>
        </router-link>
        <router-link to="/studies" class="nav-link" active-class="active">
          <span class="nav-icon">📋</span>
          <span class="nav-text">Studies</span>
        </router-link>
        <router-link to="/participants" class="nav-link" active-class="active">
          <span class="nav-icon">👥</span>
          <span class="nav-text">Participants</span>
        </router-link>
        <router-link to="/literature" class="nav-link" active-class="active">
          <span class="nav-icon">📚</span>
          <span class="nav-text">Literature</span>
        </router-link>
      </div>

      <div class="nav-user">
        <div class="user-profile">
          <div class="user-avatar">
            <span>{{ getUserInitials() }}</span>
          </div>
          <div class="user-info">
            <span class="user-name">{{ currentUser?.username || 'User' }}</span>
            <span class="user-role">Researcher</span>
          </div>
        </div>
        <button @click="handleLogout" class="logout-btn" title="Logout">
          <span class="logout-icon">🚪</span>
          <span class="logout-text">Logout</span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { auth } from "../utils/api";

const router = useRouter();
const currentUser = computed(() => auth.getCurrentUser());

const getUserInitials = () => {
  if (!currentUser.value?.username) return "U";
  return currentUser.value.username
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .substring(0, 2);
};

const handleLogout = async () => {
  await auth.logout();
  router.push("/login");
};
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 0;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  height: 70px;
}

.nav-brand {
  flex-shrink: 0;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  color: white;
  transition: opacity 0.2s;
}

.brand-link:hover {
  opacity: 0.9;
}

.brand-icon {
  font-size: 2rem;
  line-height: 1;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.brand-text {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.brand-tagline {
  font-size: 0.75rem;
  opacity: 0.9;
  font-weight: 400;
  letter-spacing: 0.5px;
}

.nav-menu {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  border-radius: 10px;
  font-weight: 500;
  font-size: 0.9375rem;
  transition: all 0.2s;
  position: relative;
  white-space: nowrap;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  transform: translateY(-1px);
}

.nav-link.active {
  background: rgba(255, 255, 255, 0.25);
  color: white;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 3px;
  background: white;
  border-radius: 2px 2px 0 0;
}

.nav-icon {
  font-size: 1.125rem;
  line-height: 1;
}

.nav-text {
  font-size: 0.9375rem;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  transition: all 0.2s;
}

.user-profile:hover {
  background: rgba(255, 255, 255, 0.2);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.875rem;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
}

.user-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: white;
  line-height: 1.2;
}

.user-role {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.2;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.625rem 1.25rem;
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.2s;
  white-space: nowrap;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.logout-icon {
  font-size: 1rem;
  line-height: 1;
}

.logout-text {
  font-size: 0.875rem;
}

/* Mobile Responsive */
@media (max-width: 1024px) {
  .nav-container {
    padding: 0 1.5rem;
    gap: 1rem;
  }

  .brand-tagline {
    display: none;
  }

  .nav-text {
    display: none;
  }

  .nav-link {
    padding: 0.75rem;
    justify-content: center;
  }

  .nav-icon {
    font-size: 1.25rem;
  }

  .user-info {
    display: none;
  }

  .logout-text {
    display: none;
  }
}

@media (max-width: 768px) {
  .nav-container {
    padding: 0 1rem;
    height: 60px;
  }

  .brand-name {
    font-size: 1rem;
  }

  .brand-icon {
    font-size: 1.5rem;
  }

  .nav-menu {
    gap: 0.25rem;
  }

  .nav-link {
    padding: 0.5rem;
  }

  .user-profile {
    padding: 0.375rem 0.75rem;
    gap: 0.5rem;
  }

  .user-avatar {
    width: 32px;
    height: 32px;
    font-size: 0.75rem;
  }

  .logout-btn {
    padding: 0.5rem 0.75rem;
  }
}

/* Animation for active link */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.nav-link.active {
  animation: slideIn 0.3s ease-out;
}
</style>
