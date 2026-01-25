<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-200 dark:from-gray-900 dark:to-gray-800 overflow-x-hidden w-full transition-colors duration-200">
    <Navbar />
    <div class="max-w-[1400px] mx-auto px-8 py-8 w-full box-border xl:px-6 md:px-4 md:py-4 sm:px-3">
      <div class="mt-55 md:mt-0 flex justify-between items-center mb-8 gap-4 flex-col md:flex-row md:gap-4 md:mb-6 sm:mb-4">
        <div>
          <h1 class="m-0 mb-2 text-gray-900 dark:text-gray-100 text-4xl font-bold break-words leading-tight md:text-3xl md:leading-snug sm:leading-snug">📊 Literature Repository</h1>
          <p class="text-gray-600 dark:text-gray-400 text-lg m-0 md:text-base">Manage and curate medical research articles</p>
        </div>
        <button 
          @click="showForm = true" 
          class="bg-gradient-to-r from-blue-500 to-blue-600 dark:from-blue-600 dark:to-blue-700 text-white border-0 w-full md:w-60 px-7 py-3.5 rounded-lg cursor-pointer text-base font-semibold flex items-center gap-2 shadow-lg transition-all hover:-translate-y-0.5 hover:shadow-xl md:justify-center md:min-h-[44px]"
        >
          <span class="text-xl">+</span> Add Article
        </button>
      </div>

      <div v-if="error" class="p-4 px-6 rounded-lg mb-6 flex items-center gap-3 font-medium bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 border-l-4 border-red-500 dark:border-red-600">
        <span class="text-xl">⚠️</span>
        {{ error }}
      </div>
      
      <div v-if="loading" class="text-center py-16 px-8 bg-white dark:bg-gray-800 rounded-xl shadow-md dark:shadow-gray-900/50">
        <div class="border-4 border-gray-200 dark:border-gray-700 border-t-blue-500 dark:border-t-blue-400 rounded-full w-12 h-12 animate-spin mx-auto mb-4"></div>
        <p class="text-gray-900 dark:text-gray-100">Loading articles...</p>
      </div>

      <!-- Articles Grid -->
      <div v-if="!loading && articles.length > 0" class="grid grid-cols-[repeat(auto-fill,minmax(300px,1fr))] gap-6 w-full md:grid-cols-[repeat(auto-fill,minmax(280px,1fr))] md:gap-5 sm:grid-cols-1 sm:gap-4">
        <div v-for="article in articles" :key="article.id" class="bg-white dark:bg-gray-800 rounded-xl shadow-md dark:shadow-gray-900/50 overflow-hidden transition-all hover:-translate-y-1 hover:shadow-lg cursor-pointer w-full max-w-full box-border" @click="viewArticle(article)">
          <div class="p-6 bg-gradient-to-r from-blue-500 to-blue-600 dark:from-blue-600 dark:to-blue-700 text-white flex justify-between items-start flex-wrap gap-3 md:p-5 sm:p-4 sm:flex-col sm:gap-2">
            <div class="flex-1 min-w-0">
              <h3 class="m-0 mb-3 text-lg font-semibold leading-snug break-words overflow-wrap-anywhere sm:text-base sm:mb-2">{{ article.title }}</h3>
              <span class="inline-block px-3.5 py-1.5 rounded-full text-xs font-semibold bg-white/30 text-white">
                {{ article.year }}
              </span>
            </div>
            <div class="flex gap-2 flex-shrink-0 sm:w-full sm:justify-end">
              <button 
                @click.stop="editArticle(article)" 
                class="bg-white/20 border-0 rounded-md p-2 cursor-pointer text-base transition-all w-8 h-8 flex items-center justify-center hover:bg-white/30 hover:scale-110 sm:min-w-[40px] sm:min-h-[40px]"
                title="Edit"
              >
                ✏️
              </button>
              <button 
                @click.stop="deleteArticle(article.id)" 
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
                <span class="text-gray-600 dark:text-gray-400 text-sm flex-shrink-0 mr-4">Authors:</span>
                <span class="text-gray-900 dark:text-gray-100 font-semibold text-right break-words">{{ article.authors }}</span>
              </div>
              <div class="flex justify-between py-3 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                <span class="text-gray-600 dark:text-gray-400 text-sm flex-shrink-0 mr-4">Journal:</span>
                <span class="text-blue-600 dark:text-blue-400 font-semibold text-right break-words">{{ article.journal }}</span>
              </div>
              <div v-if="article.doi" class="flex justify-between py-3 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                <span class="text-gray-600 dark:text-gray-400 text-sm flex-shrink-0 mr-4">DOI:</span>
                <span class="text-gray-900 dark:text-gray-100 font-semibold text-sm text-right break-words font-mono">{{ article.doi }}</span>
              </div>
            </div>
            <div v-if="article.abstract" class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <p class="text-gray-600 dark:text-gray-400 text-sm leading-relaxed m-0">{{ truncateText(article.abstract, 150) }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!loading && articles.length === 0" class="text-center py-16 px-8 bg-white dark:bg-gray-800 rounded-xl shadow-md dark:shadow-gray-900/50 sm:py-8 sm:px-4">
        <div class="text-6xl mb-4 sm:text-5xl">📚</div>
        <h3 class="m-0 mb-2 text-gray-900 dark:text-gray-100 text-2xl font-bold sm:text-xl">No Articles Yet</h3>
        <p class="text-gray-600 dark:text-gray-400 m-0 mb-6">Start building your literature repository</p>
        <button 
          @click="showForm = true" 
          class="bg-gradient-to-r from-blue-500 to-blue-600 dark:from-blue-600 dark:to-blue-700 text-white border-0 px-7 py-3.5 rounded-lg cursor-pointer text-base font-semibold flex items-center gap-2 shadow-lg transition-all hover:-translate-y-0.5 hover:shadow-xl mx-auto"
        >
          Add First Article
        </button>
      </div>
    </div>

    <!-- Article Form Modal -->
    <Teleport to="body">
      <div v-if="showForm" class="fixed inset-0 bg-black/60 dark:bg-black/70 flex items-center justify-center z-[2000] backdrop-blur-sm sm:p-0" @click="closeForm">
        <div class="bg-white dark:bg-gray-800 rounded-2xl w-[90%] max-w-[600px] max-h-[90vh] overflow-y-auto shadow-2xl" @click.stop>
          <div class="flex justify-between items-center p-6 border-b border-gray-200 dark:border-gray-700 sm:p-4 sm:sticky sm:top-0 sm:bg-white dark:sm:bg-gray-800 sm:z-10">
            <h2 class="m-0 text-gray-900 dark:text-gray-100 text-2xl font-bold sm:text-xl">{{ editingArticle ? '✏️ Edit Article' : '➕ Add Article' }}</h2>
            <button 
              @click="closeForm" 
              class="bg-transparent border-0 text-3xl text-gray-600 dark:text-gray-400 cursor-pointer w-8 h-8 flex items-center justify-center rounded-md transition-all hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-gray-100"
            >
              ×
            </button>
          </div>
          <form @submit.prevent="saveArticle" class="p-6 sm:p-4">
            <div class="mb-4">
              <label class="block mb-2 text-gray-700 dark:text-gray-300 font-semibold text-sm">Title <span class="text-red-600 dark:text-red-400">*</span></label>
              <input 
                v-model="form.title" 
                required 
                placeholder="Article title" 
                class="w-full px-3 py-3 border-2 border-gray-200 dark:border-gray-700 dark:bg-gray-700 dark:text-gray-100 rounded-lg text-base box-border transition-all focus:outline-none focus:border-blue-500 dark:focus:border-blue-400 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 sm:min-h-[44px] sm:text-base"
              />
            </div>
            <div class="grid grid-cols-2 gap-4 mb-4 sm:grid-cols-1 sm:gap-0">
              <div class="mb-4 sm:mb-4">
                <label class="block mb-2 text-gray-700 dark:text-gray-300 font-semibold text-sm">Authors <span class="text-red-600 dark:text-red-400">*</span></label>
                <input 
                  v-model="form.authors" 
                  required 
                  placeholder="e.g., Smith, J., Doe, A." 
                  class="w-full px-3 py-3 border-2 border-gray-200 dark:border-gray-700 dark:bg-gray-700 dark:text-gray-100 rounded-lg text-base box-border transition-all focus:outline-none focus:border-blue-500 dark:focus:border-blue-400 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 sm:min-h-[44px] sm:text-base"
                />
              </div>
              <div class="mb-4 sm:mb-4">
                <label class="block mb-2 text-gray-700 dark:text-gray-300 font-semibold text-sm">Journal <span class="text-red-600 dark:text-red-400">*</span></label>
                <input 
                  v-model="form.journal" 
                  required 
                  placeholder="Journal name" 
                  class="w-full px-3 py-3 border-2 border-gray-200 dark:border-gray-700 dark:bg-gray-700 dark:text-gray-100 rounded-lg text-base box-border transition-all focus:outline-none focus:border-blue-500 dark:focus:border-blue-400 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 sm:min-h-[44px] sm:text-base"
                />
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 mb-4 sm:grid-cols-1 sm:gap-0">
              <div class="mb-4 sm:mb-4">
                <label class="block mb-2 text-gray-700 dark:text-gray-300 font-semibold text-sm">Year <span class="text-red-600 dark:text-red-400">*</span></label>
                <input 
                  v-model.number="form.year" 
                  type="number" 
                  required 
                  min="1900" 
                  :max="new Date().getFullYear()" 
                  class="w-full px-3 py-3 border-2 border-gray-200 dark:border-gray-700 dark:bg-gray-700 dark:text-gray-100 rounded-lg text-base box-border transition-all focus:outline-none focus:border-blue-500 dark:focus:border-blue-400 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 sm:min-h-[44px] sm:text-base"
                />
              </div>
              <div class="mb-4 sm:mb-4">
                <label class="block mb-2 text-gray-700 dark:text-gray-300 font-semibold text-sm">DOI</label>
                <input 
                  v-model="form.doi" 
                  placeholder="10.xxxx/xxxxx" 
                  class="w-full px-3 py-3 border-2 border-gray-200 dark:border-gray-700 dark:bg-gray-700 dark:text-gray-100 rounded-lg text-base box-border transition-all focus:outline-none focus:border-blue-500 dark:focus:border-blue-400 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 sm:min-h-[44px] sm:text-base"
                />
                <small class="block mt-1 text-gray-600 dark:text-gray-400 text-xs">Must start with '10.'</small>
              </div>
            </div>
            <div class="mb-4">
              <label class="block mb-2 text-gray-700 dark:text-gray-300 font-semibold text-sm">Abstract</label>
              <textarea 
                v-model="form.abstract" 
                rows="4" 
                placeholder="Article abstract..."
                class="w-full px-3 py-3 border-2 border-gray-200 dark:border-gray-700 dark:bg-gray-700 dark:text-gray-100 rounded-lg text-base box-border transition-all focus:outline-none focus:border-blue-500 dark:focus:border-blue-400 focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 font-sans sm:min-h-[100px] sm:text-base"
              ></textarea>
            </div>
            <div class="flex gap-4 mt-6 pt-6 border-t border-gray-200 dark:border-gray-700 sm:flex-col">
              <button 
                type="submit" 
                class="bg-gradient-to-r from-blue-500 to-blue-600 dark:from-blue-600 dark:to-blue-700 text-white border-0 px-7 py-3.5 rounded-lg cursor-pointer text-base font-semibold transition-all hover:-translate-y-0.5 hover:shadow-xl flex-1 sm:w-full sm:min-h-[44px]"
              >
                💾 Save Article
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

    <!-- Article Detail Modal -->
    <Teleport to="body">
      <div v-if="viewingArticle" class="fixed inset-0 bg-black/60 dark:bg-black/70 flex items-center justify-center z-[1001] backdrop-blur-sm sm:items-start" @click="viewingArticle = null">
        <div class="bg-white dark:bg-gray-800 rounded-2xl w-[90%] max-w-[800px] max-h-[90vh] overflow-y-auto shadow-2xl" @click.stop>
          <div class="flex justify-between items-center p-6 border-b border-gray-200 dark:border-gray-700 sm:p-4 sm:sticky sm:top-0 sm:bg-white dark:sm:bg-gray-800 sm:z-10">
            <h2 class="m-0 text-gray-900 dark:text-gray-100 text-2xl font-bold sm:text-xl">{{ viewingArticle.title }}</h2>
            <button 
              @click="viewingArticle = null" 
              class="bg-transparent border-0 text-3xl text-gray-600 dark:text-gray-400 cursor-pointer w-8 h-8 flex items-center justify-center rounded-md transition-all hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-gray-100"
            >
              ×
            </button>
          </div>
          <div class="p-6 sm:p-4">
            <div class="mb-6">
              <div class="flex py-4 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                <span class="text-gray-600 dark:text-gray-400 font-semibold min-w-[120px] mr-4">📝 Authors:</span>
                <span class="text-gray-900 dark:text-gray-100 flex-1">{{ viewingArticle.authors }}</span>
              </div>
              <div class="flex py-4 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                <span class="text-gray-600 dark:text-gray-400 font-semibold min-w-[120px] mr-4">📖 Journal:</span>
                <span class="text-gray-900 dark:text-gray-100 flex-1">{{ viewingArticle.journal }}</span>
              </div>
              <div class="flex py-4 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                <span class="text-gray-600 dark:text-gray-400 font-semibold min-w-[120px] mr-4">📅 Year:</span>
                <span class="text-gray-900 dark:text-gray-100 flex-1">{{ viewingArticle.year }}</span>
              </div>
              <div v-if="viewingArticle.doi" class="flex py-4 border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                <span class="text-gray-600 dark:text-gray-400 font-semibold min-w-[120px] mr-4">🔗 DOI:</span>
                <span class="text-gray-900 dark:text-gray-100 flex-1 font-mono text-sm">{{ viewingArticle.doi }}</span>
              </div>
            </div>
            <div v-if="viewingArticle.abstract" class="mt-6 pt-6 border-t-2 border-gray-200 dark:border-gray-700">
              <h4 class="m-0 mb-4 text-gray-900 dark:text-gray-100 text-lg font-bold">Abstract</h4>
              <p class="text-gray-700 dark:text-gray-300 leading-relaxed m-0">{{ viewingArticle.abstract }}</p>
            </div>
          </div>
          <div class="p-6 border-t border-gray-200 dark:border-gray-700 flex justify-end sm:p-4">
            <button 
              @click="viewingArticle = null" 
              class="bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-0 px-7 py-3.5 rounded-lg cursor-pointer text-base font-semibold transition-all hover:bg-gray-300 dark:hover:bg-gray-600 sm:w-full sm:min-h-[44px]"
            >
              Close
            </button>
          </div>
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
