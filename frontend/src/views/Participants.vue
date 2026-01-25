<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-200 overflow-x-hidden w-full">
    <Navbar />
    <div class="max-w-[1400px] mx-auto px-8 py-8 w-full box-border xl:px-6 md:px-4 md:py-4 sm:px-3">
      <div class="mt-40 md:mt-0 flex justify-between items-center mb-8 gap-4 flex-col md:flex-row md:gap-4 md:mb-6 sm:mb-4">
        <div>
          <h1 class="m-0 mb-2 text-gray-900 text-4xl font-bold break-words leading-tight md:text-3xl md:leading-snug sm:leading-snug">👥 Study Participants</h1>
          <p class="text-gray-600 text-lg m-0 md:text-base ">Manage participant enrollment and demographics</p>

        </div>
        <button 
          @click="showForm = true" 
          class="bg-gradient-to-r from-green-500 to-green-600 text-white w-full md:w-60 border-0 px-7 py-3.5 rounded-lg cursor-pointer text-base font-semibold flex items-center gap-2 shadow-lg transition-all hover:-translate-y-0.5 hover:shadow-xl md:justify-center md:min-h-[44px]"
        >
          <span class="text-xl">+</span> Add Participant
        </button>
      </div>

      <div v-if="error" class="p-4 px-6 rounded-lg mb-6 flex items-center gap-3 font-medium bg-red-100 text-red-700 border-l-4 border-red-500">
        <span class="text-xl">⚠️</span>
        {{ error }}
      </div>
      
      <div v-if="loading" class="text-center py-16 px-8 bg-white rounded-xl shadow-md">
        <div class="border-4 border-gray-200 border-t-green-500 rounded-full w-12 h-12 animate-spin mx-auto mb-4"></div>
        <p>Loading participants...</p>
      </div>

      <!-- Participants Grid -->
      <div v-if="!loading && participants.length > 0" class="grid grid-cols-[repeat(auto-fill,minmax(300px,1fr))] gap-6 w-full md:grid-cols-[repeat(auto-fill,minmax(280px,1fr))] md:gap-5 sm:grid-cols-1 sm:gap-4">
        <div v-for="participant in participants" :key="participant.id" class="bg-white rounded-xl shadow-md overflow-hidden transition-all hover:-translate-y-1 hover:shadow-lg w-full max-w-full box-border">
          <div class="p-6 bg-gradient-to-r from-green-500 to-green-600 text-white flex justify-between items-start flex-wrap gap-3 md:p-5 sm:p-4 sm:flex-col sm:gap-2">
            <div class="flex-1 min-w-0">
              <h3 class="m-0 mb-3 text-xl font-semibold break-words overflow-wrap-anywhere sm:text-lg sm:mb-2">{{ participant.code }}</h3>
              <span class="inline-block px-3.5 py-1.5 rounded-full text-xs font-semibold uppercase tracking-wide bg-white/30 text-white">
                {{ getSexLabel(participant.sex) }}
              </span>
            </div>
            <div class="flex gap-2 flex-shrink-0 sm:w-full sm:justify-end">
              <button 
                @click="editParticipant(participant)" 
                class="bg-white/20 border-0 rounded-md p-2 cursor-pointer text-base transition-all w-8 h-8 flex items-center justify-center hover:bg-white/30 hover:scale-110 sm:min-w-[40px] sm:min-h-[40px]"
                title="Edit"
              >
                ✏️
              </button>
              <button 
                @click="deleteParticipant(participant.id)" 
                class="bg-white/20 border-0 rounded-md p-2 cursor-pointer text-base transition-all w-8 h-8 flex items-center justify-center hover:bg-white/30 hover:scale-110 sm:min-w-[40px] sm:min-h-[40px]"
                title="Delete"
              >
                🗑️
              </button>
            </div>
          </div>
          <div class="p-6 md:p-5 sm:p-4 sm:pt-5">
            <div class="mb-4 sm:mt-0">
              <div class="flex justify-between py-3 border-b border-gray-200 last:border-b-0">
                <span class="text-gray-600 text-sm">Study:</span>
                <span class="text-gray-900 font-semibold">{{ participant.study_title || 'N/A' }}</span>
              </div>
              <div class="flex justify-between py-3 border-b border-gray-200 last:border-b-0">
                <span class="text-gray-600 text-sm">Age:</span>
                <span class="text-green-600 font-semibold text-lg">{{ participant.age }} years</span>
              </div>
            </div>
            <div class="flex items-center gap-2 mt-4 pt-4 border-t border-gray-200 sm:flex-col sm:items-start">
              <span class="text-xl">📅</span>
              <div>
                <span class="block text-gray-600 text-xs uppercase tracking-wide">Enrolled:</span>
                <span class="block text-gray-900 font-semibold text-sm">{{ formatDate(participant.enrolled_on) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!loading && participants.length === 0" class="text-center py-16 px-8 bg-white rounded-xl shadow-md sm:py-8 sm:px-4">
        <div class="text-6xl mb-4 sm:text-5xl">👥</div>
        <h3 class="m-0 mb-2 text-gray-900 text-2xl font-bold sm:text-xl">No Participants Yet</h3>
        <p class="text-gray-600 m-0 mb-6">Start by enrolling participants in your studies</p>
        <button 
          @click="showForm = true" 
          class="bg-gradient-to-r from-green-500 to-green-600 text-white border-0 px-7 py-3.5 rounded-lg cursor-pointer text-base font-semibold flex items-center gap-2 shadow-lg transition-all hover:-translate-y-0.5 hover:shadow-xl mx-auto"
        >
          Enroll First Participant
        </button>
      </div>
    </div>

    <!-- Participant Form Modal -->
    <Teleport to="body">
      <div v-if="showForm" class="fixed inset-0 bg-black/60 flex items-center justify-center z-[1001] backdrop-blur-sm sm:items-start0" @click="closeForm">
        <div class="bg-white rounded-2xl w-[90%] max-w-[600px] max-h-[90vh] overflow-y-auto shadow-2xl" @click.stop>
          <div class="flex justify-between items-center p-6 border-b border-gray-200 sm:p-4 sm:sticky sm:top-0 sm:bg-white sm:z-10">
            <h2 class="m-0 text-gray-900 text-2xl font-bold sm:text-xl">{{ editingParticipant ? '✏️ Edit Participant' : '➕ Add Participant' }}</h2>
            <button 
              @click="closeForm" 
              class="bg-transparent border-0 text-3xl text-gray-600 cursor-pointer w-8 h-8 flex items-center justify-center rounded-md transition-all hover:bg-gray-100 hover:text-gray-900"
            >
              ×
            </button>
          </div>
          <form @submit.prevent="saveParticipant" class="p-6 sm:p-4">
            <div class="mb-4">
              <label class="block mb-2 text-gray-700 font-semibold text-sm">Study <span class="text-red-600">*</span></label>
              <select 
                v-model="form.study" 
                required
                class="w-full px-3 py-3 border-2 border-gray-200 rounded-lg text-base box-border transition-all focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-200 sm:min-h-[44px] sm:text-base"
              >
                <option value="">Select a study</option>
                <option v-for="study in studies" :key="study.id" :value="study.id">
                  {{ study.title }}
                </option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-4 mb-4 sm:grid-cols-1 sm:gap-0">
              <div class="mb-4 sm:mb-4">
                <label class="block mb-2 text-gray-700 font-semibold text-sm">Participant Code <span class="text-red-600">*</span></label>
                <input 
                  v-model="form.code" 
                  required 
                  placeholder="e.g., P001" 
                  class="w-full px-3 py-3 border-2 border-gray-200 rounded-lg text-base box-border transition-all focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-200 sm:min-h-[44px] sm:text-base"
                />
              </div>
              <div class="mb-4 sm:mb-4">
                <label class="block mb-2 text-gray-700 font-semibold text-sm">Age <span class="text-red-600">*</span></label>
                <input 
                  v-model.number="form.age" 
                  type="number" 
                  required 
                  min="0" 
                  max="150" 
                  placeholder="Age" 
                  class="w-full px-3 py-3 border-2 border-gray-200 rounded-lg text-base box-border transition-all focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-200 sm:min-h-[44px] sm:text-base"
                />
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 mb-4 sm:grid-cols-1 sm:gap-0">
              <div class="mb-4 sm:mb-4">
                <label class="block mb-2 text-gray-700 font-semibold text-sm">Sex <span class="text-red-600">*</span></label>
                <select 
                  v-model="form.sex" 
                  required
                  class="w-full px-3 py-3 border-2 border-gray-200 rounded-lg text-base box-border transition-all focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-200 sm:min-h-[44px] sm:text-base"
                >
                  <option value="M">👨 Male</option>
                  <option value="F">👩 Female</option>
                  <option value="Other">⚧️ Other</option>
                </select>
              </div>
              <div class="mb-4 sm:mb-4">
                <label class="block mb-2 text-gray-700 font-semibold text-sm">Enrolled On <span class="text-red-600">*</span></label>
                <input 
                  v-model="form.enrolled_on" 
                  type="date" 
                  required 
                  :max="new Date().toISOString().split('T')[0]" 
                  class="w-full px-3 py-3 border-2 border-gray-200 rounded-lg text-base box-border transition-all focus:outline-none focus:border-green-500 focus:ring-2 focus:ring-green-200 sm:min-h-[44px] sm:text-base"
                />
              </div>
            </div>
            <div class="flex gap-4 mt-6 pt-6 border-t border-gray-200 sm:flex-col">
              <button 
                type="submit" 
                class="bg-gradient-to-r from-green-500 to-green-600 text-white border-0 px-7 py-3.5 rounded-lg cursor-pointer text-base font-semibold transition-all hover:-translate-y-0.5 hover:shadow-xl flex-1 sm:w-full sm:min-h-[44px]"
              >
                💾 Save Participant
              </button>
              <button 
                type="button" 
                @click="closeForm" 
                class="bg-gray-200 text-gray-700 border-0 px-7 py-3.5 rounded-lg cursor-pointer text-base font-semibold transition-all hover:bg-gray-300 flex-1 sm:w-full sm:min-h-[44px]"
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
