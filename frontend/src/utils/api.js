const apiBase = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api";

export const fetchJson = async (url, options = {}) => {
  const response = await fetch(`${apiBase}${url}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    credentials: 'include', // Include cookies for session auth
    ...options,
  });
  
  if (!response.ok) {
    if (response.status === 401) {
      // Unauthorized - clear user and redirect to login
      localStorage.removeItem('user');
      window.location.href = '/login';
      throw new Error('Unauthorized');
    }
    const message = await response.text();
    throw new Error(message || "Request failed");
  }
  
  return response.json();
};

export const auth = {
  async login(username, password) {
    const data = await fetchJson('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
    if (data.user) {
      localStorage.setItem('user', JSON.stringify(data.user));
    }
    return data;
  },

  async signup(username, email, password, password2) {
    const data = await fetchJson('/auth/signup/', {
      method: 'POST',
      body: JSON.stringify({ username, email, password, password2 }),
    });
    return data;
  },

  async logout() {
    try {
      await fetchJson('/auth/logout/', {
        method: 'POST',
      });
    } catch (e) {
      // Ignore errors on logout
    }
    localStorage.removeItem('user');
  },

  async getUserInfo() {
    return fetchJson('/auth/user/');
  },

  isAuthenticated() {
    return !!localStorage.getItem('user');
  },

  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
};

export default { fetchJson, auth };
