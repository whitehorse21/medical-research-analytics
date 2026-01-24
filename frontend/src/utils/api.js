// Determine API base URL
// In production on Vercel, if frontend and backend are on same domain, use relative path
// Otherwise, use the environment variable or default to localhost for development
const getApiBase = () => {
  if (import.meta.env.VITE_API_BASE) {
    return import.meta.env.VITE_API_BASE;
  }
  
  // If we're on Vercel (production), try to use the same domain for API
  if (import.meta.env.PROD && window.location.hostname.includes('vercel.app')) {
    // If backend is on same domain, use relative path
    // Otherwise, you need to set VITE_API_BASE in Vercel environment variables
    return '/api';
  }
  
  // Default to localhost for development
  return "http://127.0.0.1:8000/api";
};

const apiBase = getApiBase();

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
    // Handle 404 specifically - might indicate API endpoint not found
    if (response.status === 404) {
      console.error(`API endpoint not found: ${apiBase}${url}`);
      throw new Error('API endpoint not found. Please check your API configuration.');
    }
    
    // Try to parse error message from JSON response
    let errorMessage = "Request failed";
    try {
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        const errorData = await response.json();
        errorMessage = errorData.error || errorData.message || errorMessage;
      } else {
        const text = await response.text();
        errorMessage = text || errorMessage;
      }
    } catch (e) {
      // If parsing fails, use status text
      errorMessage = response.statusText || errorMessage;
    }
    
    // Only redirect on 401 for protected routes (not login/signup)
    if (response.status === 401 && !url.includes('/auth/login/') && !url.includes('/auth/signup/')) {
      // Unauthorized - clear user and redirect to login
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    
    throw new Error(errorMessage);
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
