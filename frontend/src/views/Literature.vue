<template>
  <div class="literature-page">
    <Navbar />
    <div class="page-content">
      <div class="page-header">
        <div>
          <h1>📚 Literature Repository</h1>
          <p class="subtitle">Manage and curate medical research articles</p>
        </div>
        <button @click="showForm = true" class="btn-primary">
          <span class="btn-icon">+</span> Add Article
        </button>
      </div>

      <div v-if="error" class="alert error">
        <span class="alert-icon">⚠️</span>
        {{ error }}
      </div>
      
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>Loading articles...</p>
      </div>

      <!-- Article Form Modal -->
      <div v-if="showForm" class="modal-overlay" @click="closeForm">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ editingArticle ? '✏️ Edit Article' : '➕ Add Article' }}</h2>
            <button @click="closeForm" class="close-btn">×</button>
          </div>
          <form @submit.prevent="saveArticle">
            <div class="form-group">
              <label>Title <span class="required">*</span></label>
              <input v-model="form.title" required placeholder="Article title" />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Authors <span class="required">*</span></label>
                <input v-model="form.authors" required placeholder="e.g., Smith, J., Doe, A." />
              </div>
              <div class="form-group">
                <label>Journal <span class="required">*</span></label>
                <input v-model="form.journal" required placeholder="Journal name" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Year <span class="required">*</span></label>
                <input v-model.number="form.year" type="number" required min="1900" :max="new Date().getFullYear()" />
              </div>
              <div class="form-group">
                <label>DOI</label>
                <input v-model="form.doi" placeholder="10.xxxx/xxxxx" />
                <small class="form-hint">Must start with '10.'</small>
              </div>
            </div>
            <div class="form-group">
              <label>Abstract</label>
              <textarea v-model="form.abstract" rows="4" placeholder="Article abstract..."></textarea>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn-primary">💾 Save Article</button>
              <button type="button" @click="closeForm" class="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Articles Grid -->
      <div v-if="!loading && articles.length > 0" class="articles-grid">
        <div v-for="article in articles" :key="article.id" class="article-card" @click="viewArticle(article)">
          <div class="card-header">
            <div class="card-title-section">
              <h3>{{ article.title }}</h3>
              <span class="year-badge">{{ article.year }}</span>
            </div>
            <div class="card-actions">
              <button @click.stop="editArticle(article)" class="icon-btn edit-btn" title="Edit">
                ✏️
              </button>
              <button @click.stop="deleteArticle(article.id)" class="icon-btn delete-btn" title="Delete">
                🗑️
              </button>
            </div>
          </div>
          <div class="card-body">
            <div class="card-info">
              <div class="info-item">
                <span class="info-label">Authors:</span>
                <span class="info-value">{{ article.authors }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Journal:</span>
                <span class="info-value highlight">{{ article.journal }}</span>
              </div>
              <div v-if="article.doi" class="info-item">
                <span class="info-label">DOI:</span>
                <span class="info-value doi-link">{{ article.doi }}</span>
              </div>
            </div>
            <div v-if="article.abstract" class="abstract-preview">
              <p>{{ truncateText(article.abstract, 150) }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!loading && articles.length === 0" class="empty-state">
        <div class="empty-icon">📚</div>
        <h3>No Articles Yet</h3>
        <p>Start building your literature repository</p>
        <button @click="showForm = true" class="btn-primary">Add First Article</button>
      </div>

      <!-- Article Detail Modal -->
      <div v-if="viewingArticle" class="modal-overlay" @click="viewingArticle = null">
        <div class="modal-content large" @click.stop>
          <div class="modal-header">
            <h2>{{ viewingArticle.title }}</h2>
            <button @click="viewingArticle = null" class="close-btn">×</button>
          </div>
          <div class="article-detail">
            <div class="detail-section">
              <div class="detail-item">
                <span class="detail-label">📝 Authors:</span>
                <span class="detail-value">{{ viewingArticle.authors }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">📖 Journal:</span>
                <span class="detail-value">{{ viewingArticle.journal }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">📅 Year:</span>
                <span class="detail-value">{{ viewingArticle.year }}</span>
              </div>
              <div v-if="viewingArticle.doi" class="detail-item">
                <span class="detail-label">🔗 DOI:</span>
                <span class="detail-value doi-link">{{ viewingArticle.doi }}</span>
              </div>
            </div>
            <div v-if="viewingArticle.abstract" class="abstract-section">
              <h4>Abstract</h4>
              <p>{{ viewingArticle.abstract }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button @click="viewingArticle = null" class="btn-secondary">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import Navbar from "../components/Navbar.vue";
import { fetchJson } from "../utils/api";

const loading = ref(false);
const error = ref("");
const articles = ref([]);
const showForm = ref(false);
const editingArticle = ref(null);
const viewingArticle = ref(null);

const form = reactive({
  title: "",
  authors: "",
  journal: "",
  year: new Date().getFullYear(),
  doi: "",
  abstract: "",
});

const loadArticles = async () => {
  loading.value = true;
  error.value = "";
  try {
    const data = await fetchJson("/literature/");
    articles.value = data.results || data;
  } catch (err) {
    error.value = err.message || "Failed to load articles";
  } finally {
    loading.value = false;
  }
};

const saveArticle = async () => {
  error.value = "";
  try {
    if (editingArticle.value) {
      await fetchJson(`/literature/${editingArticle.value.id}/`, {
        method: "PATCH",
        body: JSON.stringify(form),
      });
    } else {
      await fetchJson("/literature/", {
        method: "POST",
        body: JSON.stringify(form),
      });
    }
    closeForm();
    loadArticles();
  } catch (err) {
    error.value = err.message || "Failed to save article";
  }
};

const editArticle = (article) => {
  editingArticle.value = article;
  form.title = article.title;
  form.authors = article.authors;
  form.journal = article.journal;
  form.year = article.year;
  form.doi = article.doi || "";
  form.abstract = article.abstract || "";
  showForm.value = true;
};

const viewArticle = (article) => {
  viewingArticle.value = article;
};

const deleteArticle = async (id) => {
  if (!confirm("Are you sure you want to delete this article? This action cannot be undone.")) return;
  try {
    await fetchJson(`/literature/${id}/`, { method: "DELETE" });
    loadArticles();
  } catch (err) {
    error.value = err.message || "Failed to delete article";
  }
};

const closeForm = () => {
  showForm.value = false;
  editingArticle.value = null;
  form.title = "";
  form.authors = "";
  form.journal = "";
  form.year = new Date().getFullYear();
  form.doi = "";
  form.abstract = "";
  error.value = "";
};

const truncateText = (text, maxLength) => {
  if (!text) return "";
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + "...";
};

onMounted(loadArticles);
</script>

<style scoped>
.literature-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.page-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}

.page-header h1 {
  margin: 0 0 0.5rem 0;
  color: #1a202c;
  font-size: 2rem;
  font-weight: 700;
}

.subtitle {
  color: #718096;
  margin: 0;
  font-size: 1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
  border: none;
  padding: 0.875rem 1.75rem;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 6px rgba(66, 153, 225, 0.3);
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(66, 153, 225, 0.4);
}

.btn-icon {
  font-size: 1.2rem;
}

.alert {
  padding: 1rem 1.5rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
}

.alert.error {
  background: #fed7d7;
  color: #c53030;
  border-left: 4px solid #e53e3e;
}

.alert-icon {
  font-size: 1.25rem;
}

.loading-container {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4299e1;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.article-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.card-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.card-title-section h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  line-height: 1.4;
}

.year-badge {
  display: inline-block;
  padding: 0.375rem 0.875rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.3);
  color: white;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.icon-btn {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 6px;
  padding: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

.card-body {
  padding: 1.5rem;
}

.card-info {
  margin-bottom: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  color: #718096;
  font-size: 0.875rem;
  flex-shrink: 0;
  margin-right: 1rem;
}

.info-value {
  color: #1a202c;
  font-weight: 600;
  text-align: right;
  word-break: break-word;
}

.info-value.highlight {
  color: #4299e1;
}

.doi-link {
  font-family: monospace;
  font-size: 0.875rem;
}

.abstract-preview {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.abstract-preview p {
  color: #718096;
  font-size: 0.875rem;
  line-height: 1.6;
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  color: #1a202c;
  font-size: 1.5rem;
}

.empty-state p {
  color: #718096;
  margin: 0 0 1.5rem 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.3);
}

.modal-content.large {
  max-width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h2 {
  margin: 0;
  color: #1a202c;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: #718096;
  cursor: pointer;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #f7fafc;
  color: #1a202c;
}

form {
  padding: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #4a5568;
  font-weight: 600;
  font-size: 0.875rem;
}

.required {
  color: #e53e3e;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
  transition: all 0.2s;
  font-family: inherit;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

.form-hint {
  display: block;
  margin-top: 0.25rem;
  color: #718096;
  font-size: 0.75rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.btn-secondary {
  background: #e2e8f0;
  color: #4a5568;
  border: none;
  padding: 0.875rem 1.75rem;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #cbd5e0;
}

.article-detail {
  padding: 1.5rem;
}

.detail-section {
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  padding: 1rem 0;
  border-bottom: 1px solid #e2e8f0;
}

.detail-item:last-child {
  border-bottom: none;
}

.detail-label {
  color: #718096;
  font-weight: 600;
  min-width: 120px;
  margin-right: 1rem;
}

.detail-value {
  color: #1a202c;
  flex: 1;
}

.abstract-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 2px solid #e2e8f0;
}

.abstract-section h4 {
  margin: 0 0 1rem 0;
  color: #1a202c;
  font-size: 1.125rem;
}

.abstract-section p {
  color: #4a5568;
  line-height: 1.8;
  margin: 0;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
  }

  .articles-grid {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
