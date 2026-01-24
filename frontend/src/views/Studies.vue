<template>
  <div class="studies-page">
    <Navbar />
    <div class="page-content">
      <div class="page-header">
        <div>
          <h1>📊 Clinical Studies</h1>
          <p class="subtitle">Manage and track your research studies</p>
        </div>
        <button @click="showForm = true" class="btn-primary">
          <span class="btn-icon">+</span> Add New Study
        </button>
      </div>

      <div v-if="error" class="alert error">
        <span class="alert-icon">⚠️</span>
        {{ error }}
      </div>
      
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>Loading studies...</p>
      </div>

      <!-- Study Form Modal -->
      <div v-if="showForm" class="modal-overlay" @click="closeForm">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ editingStudy ? '✏️ Edit Study' : '➕ Add New Study' }}</h2>
            <button @click="closeForm" class="close-btn">×</button>
          </div>
          <form @submit.prevent="saveStudy">
            <div class="form-row">
              <div class="form-group">
                <label>Title <span class="required">*</span></label>
                <input v-model="form.title" required placeholder="Enter study title" />
              </div>
              <div class="form-group">
                <label>Condition <span class="required">*</span></label>
                <input v-model="form.condition" required placeholder="e.g., Type 2 Diabetes" />
              </div>
            </div>
            <div class="form-group">
              <label>Status</label>
              <select v-model="form.status" @change="handleStatusChange">
                <option value="planning">📋 Planning</option>
                <option value="recruiting">👥 Recruiting</option>
                <option value="active">✅ Active</option>
                <option value="completed">✔️ Completed</option>
                <option value="cancelled">❌ Cancelled</option>
              </select>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>
                  Start Date
                  <span v-if="form.status === 'active'" class="required">*</span>
                </label>
                <input 
                  v-model="form.start_date" 
                  type="date" 
                  :required="form.status === 'active'"
                  :max="form.end_date || undefined"
                />
                <small v-if="form.status === 'active'" class="form-hint">
                  Required for active studies
                </small>
              </div>
              <div class="form-group">
                <label>
                  End Date
                  <span v-if="form.status === 'completed'" class="required">*</span>
                </label>
                <input 
                  v-model="form.end_date" 
                  type="date" 
                  :required="form.status === 'completed'"
                  :min="form.start_date || undefined"
                />
                <small v-if="form.status === 'completed'" class="form-hint">
                  Required for completed studies
                </small>
              </div>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn-primary">💾 Save Study</button>
              <button type="button" @click="closeForm" class="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Studies Grid -->
      <div v-if="!loading && studies.length > 0" class="studies-grid">
        <div v-for="study in studies" :key="study.id" class="study-card">
          <div class="card-header">
            <div class="card-title-section">
              <h3>{{ study.title }}</h3>
              <span class="status-badge" :class="study.status">
                {{ getStatusLabel(study.status) }}
              </span>
            </div>
            <div class="card-actions">
              <button @click="editStudy(study)" class="icon-btn edit-btn" title="Edit">
                ✏️
              </button>
              <button @click="deleteStudy(study.id)" class="icon-btn delete-btn" title="Delete">
                🗑️
              </button>
            </div>
          </div>
          <div class="card-body">
            <div class="card-info">
              <div class="info-item">
                <span class="info-label">Condition:</span>
                <span class="info-value">{{ study.condition }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Participants:</span>
                <span class="info-value highlight">{{ study.participant_count || 0 }}</span>
              </div>
            </div>
            <div class="card-dates">
              <div class="date-item" v-if="study.start_date">
                <span class="date-icon">📅</span>
                <div>
                  <span class="date-label">Start:</span>
                  <span class="date-value">{{ formatDate(study.start_date) }}</span>
                </div>
              </div>
              <div class="date-item" v-if="study.end_date">
                <span class="date-icon">🏁</span>
                <div>
                  <span class="date-label">End:</span>
                  <span class="date-value">{{ formatDate(study.end_date) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!loading && studies.length === 0" class="empty-state">
        <div class="empty-icon">📊</div>
        <h3>No Studies Yet</h3>
        <p>Get started by creating your first clinical study</p>
        <button @click="showForm = true" class="btn-primary">Create First Study</button>
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
const studies = ref([]);
const showForm = ref(false);
const editingStudy = ref(null);

const form = reactive({
  title: "",
  condition: "",
  status: "planning",
  start_date: "",
  end_date: "",
});

const loadStudies = async () => {
  loading.value = true;
  error.value = "";
  try {
    const data = await fetchJson("/studies/");
    studies.value = data.results || data;
  } catch (err) {
    error.value = err.message || "Failed to load studies";
  } finally {
    loading.value = false;
  }
};

const handleStatusChange = () => {
  // Auto-validate dates based on status
  if (form.status === "active" && !form.start_date) {
    // Suggest today's date for active studies
    const today = new Date().toISOString().split('T')[0];
    form.start_date = today;
  }
  if (form.status === "completed" && !form.end_date && form.start_date) {
    // Suggest end date after start date
    const start = new Date(form.start_date);
    start.setDate(start.getDate() + 1);
    form.end_date = start.toISOString().split('T')[0];
  }
};

const saveStudy = async () => {
  // Client-side validation
  if (form.status === "active" && !form.start_date) {
    error.value = "Start date is required for active studies";
    return;
  }
  if (form.status === "completed" && !form.end_date) {
    error.value = "End date is required for completed studies";
    return;
  }
  if (form.start_date && form.end_date && form.start_date > form.end_date) {
    error.value = "End date must be after start date";
    return;
  }

  error.value = "";
  try {
    if (editingStudy.value) {
      await fetchJson(`/studies/${editingStudy.value.id}/`, {
        method: "PATCH",
        body: JSON.stringify(form),
      });
    } else {
      await fetchJson("/studies/", {
        method: "POST",
        body: JSON.stringify(form),
      });
    }
    closeForm();
    loadStudies();
  } catch (err) {
    error.value = err.message || "Failed to save study";
  }
};

const editStudy = (study) => {
  editingStudy.value = study;
  form.title = study.title;
  form.condition = study.condition;
  form.status = study.status;
  form.start_date = study.start_date || "";
  form.end_date = study.end_date || "";
  showForm.value = true;
};

const deleteStudy = async (id) => {
  if (!confirm("Are you sure you want to delete this study? This action cannot be undone.")) return;
  try {
    await fetchJson(`/studies/${id}/`, { method: "DELETE" });
    loadStudies();
  } catch (err) {
    error.value = err.message || "Failed to delete study";
  }
};

const closeForm = () => {
  showForm.value = false;
  editingStudy.value = null;
  form.title = "";
  form.condition = "";
  form.status = "planning";
  form.start_date = "";
  form.end_date = "";
  error.value = "";
};

const getStatusLabel = (status) => {
  const labels = {
    planning: "Planning",
    recruiting: "Recruiting",
    active: "Active",
    completed: "Completed",
    cancelled: "Cancelled",
  };
  return labels[status] || status;
};

const formatDate = (dateString) => {
  if (!dateString) return "-";
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
};

onMounted(loadStudies);
</script>

<style scoped>
.studies-page {
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
  box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
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
  border-top: 4px solid #667eea;
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

.studies-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.study-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s;
}

.study-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.card-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.card-title-section h3 {
  margin: 0 0 0.75rem 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.status-badge {
  display: inline-block;
  padding: 0.375rem 0.875rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.planning {
  background: rgba(255, 255, 255, 0.3);
  color: white;
}

.status-badge.recruiting {
  background: rgba(59, 130, 246, 0.3);
  color: white;
}

.status-badge.active {
  background: rgba(16, 185, 129, 0.3);
  color: white;
}

.status-badge.completed {
  background: rgba(99, 102, 241, 0.3);
  color: white;
}

.status-badge.cancelled {
  background: rgba(239, 68, 68, 0.3);
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
}

.info-value {
  color: #1a202c;
  font-weight: 600;
}

.info-value.highlight {
  color: #667eea;
  font-size: 1.125rem;
}

.card-dates {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.date-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
}

.date-icon {
  font-size: 1.25rem;
}

.date-label {
  display: block;
  color: #718096;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.date-value {
  display: block;
  color: #1a202c;
  font-weight: 600;
  font-size: 0.875rem;
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
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
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

@media (max-width: 1024px) {
  .page-content {
    padding: 1.5rem;
  }

  .studies-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }
}

@media (max-width: 768px) {
  .page-content {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }

  .btn-primary {
    width: 100%;
    justify-content: center;
  }

  .studies-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .study-card {
    margin: 0;
  }

  .card-header {
    padding: 1rem;
  }

  .card-body {
    padding: 1rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-content {
    width: 95%;
    max-width: none;
    margin: 1rem;
  }

  .modal-header {
    padding: 1rem;
  }

  form {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .page-content {
    padding: 0.75rem;
  }

  .page-header h1 {
    font-size: 1.25rem;
  }

  .subtitle {
    font-size: 0.875rem;
  }

  .card-header {
    flex-direction: column;
    gap: 0.75rem;
  }

  .card-title-section {
    width: 100%;
  }

  .card-actions {
    align-self: flex-end;
  }

  .modal-content {
    width: 100%;
    margin: 0;
    border-radius: 0;
    max-height: 100vh;
  }

  .modal-overlay {
    padding: 0;
  }
}
</style>
