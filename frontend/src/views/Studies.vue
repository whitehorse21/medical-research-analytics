<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-200 dark:from-gray-900 dark:to-gray-800 overflow-x-hidden w-full transition-colors duration-200">
    <Navbar />
    <div class="max-w-[1400px] mx-auto px-8 py-8 w-full box-border xl:px-6 md:px-4 md:py-4 sm:px-3">
      <div class="mt-55 md:mt-0 flex justify-between items-center mb-8 gap-4 flex-col md:flex-row md:gap-4 md:mb-6 sm:mb-4">
        <div>
          <h1 class="m-0 mb-2 text-gray-900 dark:text-gray-100 text-4xl font-bold break-words leading-tight md:text-3xl md:leading-snug sm:leading-snug">📋 Clinical Studies</h1>
          <p class="text-gray-600 dark:text-gray-400 text-lg m-0 md:text-base">Manage and track your research studies</p>
        </div>
        <button 
          @click="showForm = true" 
          class="bg-gradient-to-r from-indigo-500 to-purple-600 dark:from-indigo-600 dark:to-purple-700 text-white border-0 w-full md:w-60 px-7 py-3.5 rounded-lg cursor-pointer text-base font-semibold flex items-center gap-2 shadow-lg transition-all hover:-translate-y-0.5 hover:shadow-xl md:justify-center md:min-h-[44px]"
        >
          <span class="text-xl">+</span> Add New Study
        </button>
      </div>

      <div v-if="error" class="p-4 px-6 rounded-lg mb-6 flex items-center gap-3 font-medium bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 border-l-4 border-red-500 dark:border-red-600">
        <span class="text-xl">⚠️</span>
        {{ error }}
      </div>
      
      <div v-if="loading" class="text-center py-16 px-8 bg-white dark:bg-gray-800 rounded-xl shadow-md dark:shadow-gray-900/50">
        <div class="border-4 border-gray-200 dark:border-gray-700 border-t-indigo-500 dark:border-t-indigo-400 rounded-full w-12 h-12 animate-spin mx-auto mb-4"></div>
        <p class="text-gray-900 dark:text-gray-100">Loading studies...</p>
      </div>

      <!-- Studies Grid -->
      <div v-if="!loading && studies.length > 0" class="grid grid-cols-[repeat(auto-fill,minmax(300px,1fr))] gap-6 w-full md:grid-cols-[repeat(auto-fill,minmax(280px,1fr))] md:gap-5 sm:grid-cols-1 sm:gap-4">
        <div v-for="study in studies" :key="study.id" class="bg-white dark:bg-gray-800 rounded-xl shadow-md dark:shadow-gray-900/50 overflow-hidden transition-all hover:-translate-y-1 hover:shadow-lg w-full max-w-full box-border">
          <div class="p-6 bg-gradient-to-r from-indigo-500 to-purple-600 dark:from-indigo-600 dark:to-purple-700 text-white flex justify-between items-start flex-wrap gap-3 md:p-5 sm:p-4 sm:flex-col sm:gap-2">
            <div class="flex-1 min-w-0">
              <h3 class="m-0 mb-3 text-xl font-semibold break-words overflow-wrap-anywhere sm:text-lg sm:mb-2">{{ study.title }}</h3>
              <span 
                class="inline-block px-3.5 py-1.5 rounded-full text-xs font-semibold uppercase tracking-wide"
                :class="{
                  'bg-white/30': study.status === 'planning',
                  'bg-blue-500/30': study.status === 'recruiting',
                  'bg-green-500/30': study.status === 'active',
                  'bg-indigo-500/30': study.status === 'completed',
                  'bg-red-500/30': study.status === 'cancelled'
                }"
              >
                {{ getStatusLabel(study.status) }}
              </span>
            </div>
            <div class="flex gap-2 flex-shrink-0 sm:w-full sm:justify-end">
              <button 
                @click="editStudy(study)" 
                class="bg-white/20 border-0 rounded-md p-2 cursor-pointer text-base transition-all w-8 h-8 flex items-center justify-center hover:bg-white/30 hover:scale-110 sm:min-w-[40px] sm:min-h-[40px]"
                title="Edit"
              >
                ✏️
              </button>
              <button 
                @click="deleteStudy(study.id)" 
                class="bg-white/20 border-0 rounded-md p-2 cursor-pointer text-base transition-all w-8 h-8 flex items-center justify-center hover:bg-white/30 hover:scale-110 sm:min-w-[40px] sm:min-h-[40px]"
                title="Delete"
              >
                🗑️
              </button>
            </div>
          </div>
          <div class="p-6 md:p-5 sm:p-4 sm:pt-5">
            <div class="mb-4 sm:mt-0">
              <div class="flex justify-between py-3 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                <span class="text-gray-600 dark:text-gray-400 text-sm">Condition:</span>
                <span class="text-gray-900 dark:text-gray-100 font-semibold">{{ study.condition }}</span>
              </div>
              <div class="flex justify-between py-3 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                <span class="text-gray-600 dark:text-gray-400 text-sm">Participants:</span>
                <span class="text-indigo-600 dark:text-indigo-400 font-semibold text-lg">{{ study.participant_count || 0 }}</span>
              </div>
            </div>
            <div class="flex gap-4 mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 sm:flex-col sm:gap-2">
              <div v-if="study.start_date" class="flex items-center gap-2 flex-1 sm:w-full">
                <span class="text-xl">📅</span>
                <div>
                  <span class="block text-gray-600 dark:text-gray-400 text-xs uppercase tracking-wide">Start:</span>
                  <span class="block text-gray-900 dark:text-gray-100 font-semibold text-sm">{{ formatDate(study.start_date) }}</span>
                </div>
              </div>
              <div v-if="study.end_date" class="flex items-center gap-2 flex-1 sm:w-full">
                <span class="text-xl">🏁</span>
                <div>
                  <span class="block text-gray-600 dark:text-gray-400 text-xs uppercase tracking-wide">End:</span>
                  <span class="block text-gray-900 dark:text-gray-100 font-semibold text-sm">{{ formatDate(study.end_date) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!loading && studies.length === 0" class="text-center py-16 px-8 bg-white dark:bg-gray-800 rounded-xl shadow-md dark:shadow-gray-900/50 sm:py-8 sm:px-4">
        <div class="text-6xl mb-4 sm:text-5xl">📊</div>
        <h3 class="m-0 mb-2 text-gray-900 dark:text-gray-100 text-2xl font-bold sm:text-xl">No Studies Yet</h3>
        <p class="text-gray-600 dark:text-gray-400 m-0 mb-6">Get started by creating your first clinical study</p>
        <button 
          @click="showForm = true" 
          class="bg-gradient-to-r from-indigo-500 to-purple-600 dark:from-indigo-600 dark:to-purple-700 text-white border-0 px-7 py-3.5 rounded-lg cursor-pointer text-base font-semibold flex items-center gap-2 shadow-lg transition-all hover:-translate-y-0.5 hover:shadow-xl mx-auto"
        >
          Create First Study
        </button>
      </div>
    </div>

    <!-- Study Form Modal -->
    <Teleport to="body">
      <div v-if="showForm" class="fixed inset-0 bg-black/60 dark:bg-black/70 flex items-center justify-center z-[1001] backdrop-blur-sm" @click="closeForm">
        <div class="bg-white dark:bg-gray-800 rounded-2xl w-[90%] max-w-[600px] max-h-[90vh] overflow-y-auto shadow-2xl" @click.stop>
          <div class="flex justify-between items-center p-6 border-b border-gray-200 dark:border-gray-700 sm:p-4 sm:sticky sm:top-0 sm:bg-white dark:sm:bg-gray-800 sm:z-10">
            <h2 class="m-0 text-gray-900 dark:text-gray-100 text-2xl font-bold sm:text-xl">{{ editingStudy ? '✏️ Edit Study' : '➕ Add New Study' }}</h2>
            <button 
              @click="closeForm" 
              class="bg-transparent border-0 text-3xl text-gray-600 dark:text-gray-400 cursor-pointer w-8 h-8 flex items-center justify-center rounded-md transition-all hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-gray-100"
            >
              ×
            </button>
          </div>
          <form @submit.prevent="saveStudy" class="p-6 sm:p-4">
            <div class="grid grid-cols-2 gap-4 mb-4 sm:grid-cols-1 sm:gap-0">
              <div class="mb-4 sm:mb-4">
                <label class="block mb-2 text-gray-700 dark:text-gray-300 font-semibold text-sm">Title <span class="text-red-600 dark:text-red-400">*</span></label>
                <input 
                  v-model="form.title" 
                  required 
                  placeholder="Enter study title" 
                  class="w-full px-3 py-3 border-2 border-gray-200 dark:border-gray-700 dark:bg-gray-700 dark:text-gray-100 rounded-lg text-base box-border transition-all focus:outline-none focus:border-indigo-500 dark:focus:border-indigo-400 focus:ring-2 focus:ring-indigo-200 dark:focus:ring-indigo-800 sm:min-h-[44px] sm:text-base"
                />
              </div>
              <div class="mb-4 sm:mb-4">
                <label class="block mb-2 text-gray-700 dark:text-gray-300 font-semibold text-sm">Condition <span class="text-red-600 dark:text-red-400">*</span></label>
                <input 
                  v-model="form.condition" 
                  required 
                  placeholder="e.g., Type 2 Diabetes" 
                  class="w-full px-3 py-3 border-2 border-gray-200 dark:border-gray-700 dark:bg-gray-700 dark:text-gray-100 rounded-lg text-base box-border transition-all focus:outline-none focus:border-indigo-500 dark:focus:border-indigo-400 focus:ring-2 focus:ring-indigo-200 dark:focus:ring-indigo-800 sm:min-h-[44px] sm:text-base"
                />
              </div>
            </div>
            <div class="mb-4">
              <label class="block mb-2 text-gray-700 dark:text-gray-300 font-semibold text-sm">Status</label>
              <select 
                v-model="form.status" 
                @change="handleStatusChange"
                class="w-full px-3 py-3 border-2 border-gray-200 dark:border-gray-700 dark:bg-gray-700 dark:text-gray-100 rounded-lg text-base box-border transition-all focus:outline-none focus:border-indigo-500 dark:focus:border-indigo-400 focus:ring-2 focus:ring-indigo-200 dark:focus:ring-indigo-800 sm:min-h-[44px] sm:text-base"
              >
                <option value="planning">📋 Planning</option>
                <option value="recruiting">👥 Recruiting</option>
                <option value="active">✅ Active</option>
                <option value="completed">✔️ Completed</option>
                <option value="cancelled">❌ Cancelled</option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-4 mb-4 sm:grid-cols-1 sm:gap-0">
              <div class="mb-4 sm:mb-4">
                <label class="block mb-2 text-gray-700 dark:text-gray-300 font-semibold text-sm">
                  Start Date
                  <span v-if="form.status === 'active'" class="text-red-600 dark:text-red-400">*</span>
                </label>
                <input 
                  v-model="form.start_date" 
                  type="date" 
                  :required="form.status === 'active'"
                  :max="form.end_date || undefined"
                  class="w-full px-3 py-3 border-2 border-gray-200 dark:border-gray-700 dark:bg-gray-700 dark:text-gray-100 rounded-lg text-base box-border transition-all focus:outline-none focus:border-indigo-500 dark:focus:border-indigo-400 focus:ring-2 focus:ring-indigo-200 dark:focus:ring-indigo-800 sm:min-h-[44px] sm:text-base"
                />
                <small v-if="form.status === 'active'" class="block mt-1 text-gray-600 dark:text-gray-400 text-xs">
                  Required for active studies
                </small>
              </div>
              <div class="mb-4 sm:mb-4">
                <label class="block mb-2 text-gray-700 dark:text-gray-300 font-semibold text-sm">
                  End Date
                  <span v-if="form.status === 'completed'" class="text-red-600 dark:text-red-400">*</span>
                </label>
                <input 
                  v-model="form.end_date" 
                  type="date" 
                  :required="form.status === 'completed'"
                  :min="form.start_date || undefined"
                  class="w-full px-3 py-3 border-2 border-gray-200 dark:border-gray-700 dark:bg-gray-700 dark:text-gray-100 rounded-lg text-base box-border transition-all focus:outline-none focus:border-indigo-500 dark:focus:border-indigo-400 focus:ring-2 focus:ring-indigo-200 dark:focus:ring-indigo-800 sm:min-h-[44px] sm:text-base"
                />
                <small v-if="form.status === 'completed'" class="block mt-1 text-gray-600 dark:text-gray-400 text-xs">
                  Required for completed studies
                </small>
              </div>
            </div>
            <div class="flex gap-4 mt-6 pt-6 border-t border-gray-200 dark:border-gray-700 sm:flex-col">
              <button 
                type="submit" 
                class="bg-gradient-to-r from-indigo-500 to-purple-600 dark:from-indigo-600 dark:to-purple-700 text-white border-0 px-7 py-3.5 rounded-lg cursor-pointer text-base font-semibold transition-all hover:-translate-y-0.5 hover:shadow-xl flex-1 sm:w-full sm:min-h-[44px]"
              >
                💾 Save Study
              </button>
              <button 
                type="button" 
                @click="closeForm" 
                class="bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-0 px-7 py-3.5 rounded-lg cursor-pointer text-base font-semibold transition-all hover:bg-gray-300 dark:hover:bg-gray-600 flex-1 sm:w-full sm:min-h-[44px]"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
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
