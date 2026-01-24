<template>
  <div class="participants-page">
    <Navbar />
    <div class="page-content">
      <div class="page-header">
        <div>
          <h1>👥 Study Participants</h1>
          <p class="subtitle">Manage participant enrollment and demographics</p>
        </div>
        <button @click="showForm = true" class="btn-primary">
          <span class="btn-icon">+</span> Add Participant
        </button>
      </div>

      <div v-if="error" class="alert error">
        <span class="alert-icon">⚠️</span>
        {{ error }}
      </div>
      
      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>Loading participants...</p>
      </div>

      <!-- Participant Form Modal -->
      <div v-if="showForm" class="modal-overlay" @click="closeForm">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ editingParticipant ? '✏️ Edit Participant' : '➕ Add Participant' }}</h2>
            <button @click="closeForm" class="close-btn">×</button>
          </div>
          <form @submit.prevent="saveParticipant">
            <div class="form-group">
              <label>Study <span class="required">*</span></label>
              <select v-model="form.study" required>
                <option value="">Select a study</option>
                <option v-for="study in studies" :key="study.id" :value="study.id">
                  {{ study.title }}
                </option>
              </select>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Participant Code <span class="required">*</span></label>
                <input v-model="form.code" required placeholder="e.g., P001" />
              </div>
              <div class="form-group">
                <label>Age <span class="required">*</span></label>
                <input v-model.number="form.age" type="number" required min="0" max="150" placeholder="Age" />
              </div>
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Sex <span class="required">*</span></label>
                <select v-model="form.sex" required>
                  <option value="M">👨 Male</option>
                  <option value="F">👩 Female</option>
                  <option value="Other">⚧️ Other</option>
                </select>
              </div>
              <div class="form-group">
                <label>Enrolled On <span class="required">*</span></label>
                <input v-model="form.enrolled_on" type="date" required :max="new Date().toISOString().split('T')[0]" />
              </div>
            </div>
            <div class="form-actions">
              <button type="submit" class="btn-primary">💾 Save Participant</button>
              <button type="button" @click="closeForm" class="btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Participants Grid -->
      <div v-if="!loading && participants.length > 0" class="participants-grid">
        <div v-for="participant in participants" :key="participant.id" class="participant-card">
          <div class="card-header">
            <div class="card-title-section">
              <h3>{{ participant.code }}</h3>
              <span class="sex-badge" :class="participant.sex.toLowerCase()">
                {{ getSexLabel(participant.sex) }}
              </span>
            </div>
            <div class="card-actions">
              <button @click="editParticipant(participant)" class="icon-btn edit-btn" title="Edit">
                ✏️
              </button>
              <button @click="deleteParticipant(participant.id)" class="icon-btn delete-btn" title="Delete">
                🗑️
              </button>
            </div>
          </div>
          <div class="card-body">
            <div class="card-info">
              <div class="info-item">
                <span class="info-label">Study:</span>
                <span class="info-value">{{ participant.study_title || 'N/A' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Age:</span>
                <span class="info-value highlight">{{ participant.age }} years</span>
              </div>
            </div>
            <div class="enrollment-date">
              <span class="date-icon">📅</span>
              <div>
                <span class="date-label">Enrolled:</span>
                <span class="date-value">{{ formatDate(participant.enrolled_on) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!loading && participants.length === 0" class="empty-state">
        <div class="empty-icon">👥</div>
        <h3>No Participants Yet</h3>
        <p>Start by enrolling participants in your studies</p>
        <button @click="showForm = true" class="btn-primary">Enroll First Participant</button>
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
const participants = ref([]);
const studies = ref([]);
const showForm = ref(false);
const editingParticipant = ref(null);

const form = reactive({
  study: "",
  code: "",
  age: "",
  sex: "M",
  enrolled_on: "",
});

const loadData = async () => {
  loading.value = true;
  error.value = "";
  try {
    const [participantsData, studiesData] = await Promise.all([
      fetchJson("/participants/"),
      fetchJson("/studies/"),
    ]);
    participants.value = participantsData.results || participantsData;
    studies.value = studiesData.results || studiesData;
  } catch (err) {
    error.value = err.message || "Failed to load data";
  } finally {
    loading.value = false;
  }
};

const saveParticipant = async () => {
  error.value = "";
  try {
    if (editingParticipant.value) {
      await fetchJson(`/participants/${editingParticipant.value.id}/`, {
        method: "PATCH",
        body: JSON.stringify(form),
      });
    } else {
      await fetchJson("/participants/", {
        method: "POST",
        body: JSON.stringify(form),
      });
    }
    closeForm();
    loadData();
  } catch (err) {
    error.value = err.message || "Failed to save participant";
  }
};

const editParticipant = (participant) => {
  editingParticipant.value = participant;
  form.study = participant.study;
  form.code = participant.code;
  form.age = participant.age;
  form.sex = participant.sex;
  form.enrolled_on = participant.enrolled_on;
  showForm.value = true;
};

const deleteParticipant = async (id) => {
  if (!confirm("Are you sure you want to delete this participant? This action cannot be undone.")) return;
  try {
    await fetchJson(`/participants/${id}/`, { method: "DELETE" });
    loadData();
  } catch (err) {
    error.value = err.message || "Failed to delete participant";
  }
};

const closeForm = () => {
  showForm.value = false;
  editingParticipant.value = null;
  form.study = "";
  form.code = "";
  form.age = "";
  form.sex = "M";
  form.enrolled_on = "";
  error.value = "";
};

const getSexLabel = (sex) => {
  const labels = { M: "Male", F: "Female", Other: "Other" };
  return labels[sex] || sex;
};

const formatDate = (dateString) => {
  if (!dateString) return "-";
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
};

onMounted(loadData);
</script>

<style scoped>
.participants-page {
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
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
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
  box-shadow: 0 4px 6px rgba(72, 187, 120, 0.3);
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(72, 187, 120, 0.4);
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
  border-top: 4px solid #48bb78;
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

.participants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.participant-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s;
}

.participant-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.card-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
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

.sex-badge {
  display: inline-block;
  padding: 0.375rem 0.875rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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
}

.info-value {
  color: #1a202c;
  font-weight: 600;
}

.info-value.highlight {
  color: #48bb78;
  font-size: 1.125rem;
}

.enrollment-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
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
  border-color: #48bb78;
  box-shadow: 0 0 0 3px rgba(72, 187, 120, 0.1);
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

  .participants-grid {
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

  .participants-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .participant-card {
    margin: 0;
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
}
  .page-header {
    flex-direction: column;
    gap: 1rem;
  }

  .participants-grid {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
