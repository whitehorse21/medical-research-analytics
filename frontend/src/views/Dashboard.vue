<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-blue-200 overflow-x-hidden w-full">
    <Navbar />
    <div class="max-w-[1400px] mx-auto px-8 py-8 w-full box-border xl:px-6 md:px-4 md:py-4 sm:px-3">
      <div class="mt-40 md:mt-0 flex justify-between items-center mb-8 gap-4 flex-col md:flex-row md:gap-4 md:mb-6 sm:mb-4">
        <div>
          <h1 class="m-0 mb-2 text-gray-900 text-4xl font-bold break-words leading-tight md:text-3xl md:leading-snug sm:leading-snug">Research Analytics Dashboard</h1>
          <p class="text-gray-600 text-lg m-0 md:text-base ">Comprehensive overview of your medical research platform</p>
        </div>
        <button 
          @click="loadStats" 
          :disabled="loading"
          class="bg-white border-2 border-indigo-500 text-indigo-500 w-full md:w-60 px-6 py-3 rounded-lg cursor-pointer text-base font-semibold transition-all hover:bg-indigo-500 hover:text-white disabled:opacity-60 disabled:cursor-not-allowed md:justify-center md:min-h-[44px]"
        >
          <span v-if="!loading">↻ Refresh</span>
          <span v-else>Loading...</span>
        </button>
      </div>

      <div v-if="loading" class="text-center py-16 px-8 bg-white rounded-xl shadow-md">
        <div class="border-4 border-gray-200 border-t-indigo-500 rounded-full w-12 h-12 animate-spin mx-auto mb-4"></div>
        <p>Loading analytics...</p>
      </div>
      <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded-lg mb-8 text-center font-medium">{{ error }}</div>
      
      <div v-if="!loading && !error" class="flex flex-col gap-6">
        <!-- Key Metrics Row -->
        <div class="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-6 md:grid-cols-2 md:gap-5 sm:grid-cols-1 sm:gap-4">
          <div class="bg-white p-6 rounded-xl shadow-md flex items-center gap-4 transition-all hover:-translate-y-0.5 hover:shadow-lg border-l-4 border-indigo-500">
            <div class="text-4xl">📊</div>
            <div class="flex-1">
              <div class="text-gray-600 text-sm font-medium uppercase tracking-wide">Total Studies</div>
              <div class="text-gray-900 text-3xl font-bold my-2 sm:text-2xl">{{ studyStats.total_studies || 0 }}</div>
              <div class="flex items-center gap-2 text-sm">
                <span class="text-green-600 font-semibold">+{{ studyStats.recent_studies || 0 }}</span>
                <span class="text-gray-400">new this month</span>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl shadow-md flex items-center gap-4 transition-all hover:-translate-y-0.5 hover:shadow-lg border-l-4 border-green-500">
            <div class="text-4xl">👥</div>
            <div class="flex-1">
              <div class="text-gray-600 text-sm font-medium uppercase tracking-wide">Total Participants</div>
              <div class="text-gray-900 text-3xl font-bold my-2 sm:text-2xl">{{ participantStats.total_participants || 0 }}</div>
              <div class="flex items-center gap-2 text-sm">
                <span class="text-green-600 font-semibold">+{{ participantStats.recent_enrollments || 0 }}</span>
                <span class="text-gray-400">enrolled this month</span>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl shadow-md flex items-center gap-4 transition-all hover:-translate-y-0.5 hover:shadow-lg border-l-4 border-blue-500">
            <div class="text-4xl">📚</div>
            <div class="flex-1">
              <div class="text-gray-600 text-sm font-medium uppercase tracking-wide">Literature Articles</div>
              <div class="text-gray-900 text-3xl font-bold my-2 sm:text-2xl">{{ literatureStats.total_articles || 0 }}</div>
              <div class="flex items-center gap-2 text-sm">
                <span class="text-green-600 font-semibold">+{{ literatureStats.recent_articles || 0 }}</span>
                <span class="text-gray-400">added this month</span>
              </div>
            </div>
          </div>

          <div class="bg-white p-6 rounded-xl shadow-md flex items-center gap-4 transition-all hover:-translate-y-0.5 hover:shadow-lg border-l-4 border-orange-500">
            <div class="text-4xl">✅</div>
            <div class="flex-1">
              <div class="text-gray-600 text-sm font-medium uppercase tracking-wide">Completion Rate</div>
              <div class="text-gray-900 text-3xl font-bold my-2 sm:text-2xl">{{ studyStats.completion_rate || 0 }}%</div>
              <div class="flex items-center gap-2 text-sm">
                <span>{{ studyStats.completed_studies || 0 }} of {{ studyStats.total_studies || 0 }}</span>
                <span class="text-gray-400">studies completed</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Studies Analytics -->
        <div class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="flex justify-between items-center p-6 border-b border-gray-200 md:flex-col md:items-start md:gap-4 md:flex-wrap">
            <h2 class="m-0 text-gray-900 text-2xl font-semibold md:text-xl sm:text-lg break-words">Studies Overview</h2>
            <router-link to="/studies" class="text-indigo-500 no-underline font-medium transition-colors hover:text-indigo-600">View All →</router-link>
          </div>
          <div class="p-6 md:p-6 sm:p-4 pt-5">
            <div class="grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-8 w-full lg:grid-cols-1 lg:gap-6">
              <div class="md:pb-4">
                <div class="text-gray-700 text-base font-semibold mb-4 uppercase tracking-wide sm:text-sm">Status Distribution</div>
                <div class="flex flex-col gap-4 pt-5 md:pt-5 sm:pt-5">
                  <div v-for="(count, status) in studyStats.by_status" :key="status" class="flex flex-col gap-2">
                    <div class="flex justify-between items-center">
                      <span class="text-gray-700 font-medium capitalize">{{ status.charAt(0).toUpperCase() + status.slice(1) }}</span>
                      <span class="text-gray-900 font-semibold">{{ count }}</span>
                    </div>
                    <div class="h-2 bg-gray-200 rounded overflow-hidden">
                      <div 
                        class="h-full rounded transition-all duration-300"
                        :class="{
                          'bg-amber-400': status === 'planning',
                          'bg-blue-500': status === 'recruiting',
                          'bg-green-500': status === 'active',
                          'bg-indigo-500': status === 'completed',
                          'bg-red-500': status === 'cancelled'
                        }"
                        :style="{ width: `${(count / (studyStats.total_studies || 1)) * 100}%` }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="md:pb-4">
                <div class="text-gray-700 text-base font-semibold mb-4 uppercase tracking-wide sm:text-sm">Key Metrics</div>
                <div class="flex flex-col gap-4">
                  <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span class="text-gray-600 text-sm">Active Studies</span>
                    <span class="text-indigo-500 font-semibold text-xl">{{ studyStats.active_studies || 0 }}</span>
                  </div>
                  <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span class="text-gray-600 text-sm">Ongoing Studies</span>
                    <span class="text-gray-900 font-semibold text-lg">{{ studyStats.ongoing_studies || 0 }}</span>
                  </div>
                  <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span class="text-gray-600 text-sm">Studies with Dates</span>
                    <span class="text-gray-900 font-semibold text-lg">{{ studyStats.studies_with_dates || 0 }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Participants Analytics -->
        <div class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="flex justify-between items-center p-6 border-b border-gray-200 md:flex-col md:items-start md:gap-4 md:flex-wrap">
            <h2 class="m-0 text-gray-900 text-2xl font-semibold md:text-xl sm:text-lg break-words">Participants Analytics</h2>
            <router-link to="/participants" class="text-indigo-500 no-underline font-medium transition-colors hover:text-indigo-600">View All →</router-link>
          </div>
          <div class="p-6 md:p-6 sm:p-4 pt-5">
            <div class="grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-8 w-full lg:grid-cols-1 lg:gap-6">
              <div class="md:pb-4">
                <div class="text-gray-700 text-base font-semibold mb-4 uppercase tracking-wide sm:text-sm">Demographics</div>
                <div class="flex flex-col gap-4 mb-6">
                  <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span class="text-gray-600 text-sm">Average Age</span>
                    <span class="text-gray-900 font-semibold">{{ participantStats.average_age || 0 }} years</span>
                  </div>
                  <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span class="text-gray-600 text-sm">Age Range</span>
                    <span class="text-gray-900 font-semibold">{{ participantStats.min_age || 0 }} - {{ participantStats.max_age || 0 }} years</span>
                  </div>
                  <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span class="text-gray-600 text-sm">Avg per Study</span>
                    <span class="text-gray-900 font-semibold">{{ participantStats.average_per_study || 0 }}</span>
                  </div>
                </div>
                <div class="flex flex-col gap-3 pt-5 md:pt-5 sm:pt-5">
                  <div v-for="(count, sex) in participantStats.by_sex" :key="sex" class="flex flex-col gap-2">
                    <div class="h-6 bg-gray-200 rounded-xl overflow-hidden relative">
                      <div 
                        class="h-full bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl transition-all duration-300"
                        :style="{ width: `${(count / (participantStats.total_participants || 1)) * 100}%` }"
                      ></div>
                    </div>
                    <div class="flex justify-between text-sm">
                      <span class="text-gray-700 font-medium">{{ sex }}</span>
                      <span class="text-gray-900 font-semibold">{{ count }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="md:pb-4">
                <div class="text-gray-700 text-base font-semibold mb-4 uppercase tracking-wide sm:text-sm">Age Groups</div>
                <div class="flex flex-col gap-4 pt-5 md:pt-5 sm:pt-5">
                  <div v-for="(count, group) in participantStats.age_groups" :key="group" class="flex flex-col gap-2">
                    <div class="flex justify-between items-center">
                      <span class="text-gray-700 font-medium text-sm">{{ group }} years</span>
                      <span class="text-gray-900 font-semibold">{{ count }}</span>
                    </div>
                    <div class="h-2 bg-gray-200 rounded overflow-hidden">
                      <div 
                        class="h-full bg-indigo-500 rounded transition-all duration-300"
                        :style="{ width: `${(count / (participantStats.total_participants || 1)) * 100}%` }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Literature Analytics -->
        <div class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="flex justify-between items-center p-6 border-b border-gray-200 md:flex-col md:items-start md:gap-4 md:flex-wrap">
            <h2 class="m-0 text-gray-900 text-2xl font-semibold md:text-xl sm:text-lg break-words">Literature Repository</h2>
            <router-link to="/literature" class="text-indigo-500 no-underline font-medium transition-colors hover:text-indigo-600">View All →</router-link>
          </div>
          <div class="p-6 md:p-6 sm:p-4 pt-5">
            <div class="grid grid-cols-[repeat(auto-fit,minmax(300px,1fr))] gap-8 w-full lg:grid-cols-1 lg:gap-6">
              <div class="md:pb-4">
                <div class="text-gray-700 text-base font-semibold mb-4 uppercase tracking-wide sm:text-sm">Publication Trends</div>
                <div class="flex flex-col gap-4 mb-6">
                  <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span class="text-gray-600 text-sm">Current Year ({{ new Date().getFullYear() }})</span>
                    <span class="text-gray-900 font-semibold text-lg">{{ literatureStats.current_year_articles || 0 }}</span>
                  </div>
                  <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span class="text-gray-600 text-sm">Last Year ({{ new Date().getFullYear() - 1 }})</span>
                    <span class="text-gray-900 font-semibold text-lg">{{ literatureStats.last_year_articles || 0 }}</span>
                  </div>
                  <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span class="text-gray-600 text-sm">DOI Coverage</span>
                    <span class="text-gray-900 font-semibold text-lg">{{ literatureStats.doi_coverage || 0 }}%</span>
                  </div>
                </div>
                <div v-if="literatureStats.year_range" class="p-4 bg-gray-100 rounded-lg text-center">
                  <span class="text-gray-600 text-sm mr-2">Publication Range:</span>
                  <span class="text-gray-900 font-semibold">{{ literatureStats.year_range.min_year || 'N/A' }} - {{ literatureStats.year_range.max_year || 'N/A' }}</span>
                </div>
              </div>
              <div class="md:pb-4">
                <div class="text-gray-700 text-base font-semibold mb-4 uppercase tracking-wide sm:text-sm">Top Journals</div>
                <div class="flex flex-col gap-3">
                  <div 
                    v-for="(journal, index) in (literatureStats.top_journals || []).slice(0, 5)" 
                    :key="index" 
                    class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg transition-colors hover:bg-gray-100"
                  >
                    <div class="w-8 h-8 bg-indigo-500 text-white rounded-full flex items-center justify-center font-semibold text-sm">{{ index + 1 }}</div>
                    <div class="flex-1 flex flex-col gap-1">
                      <span class="text-gray-900 font-medium text-sm">{{ journal.journal }}</span>
                      <span class="text-gray-600 text-xs">{{ journal.count }} articles</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Navbar from "../components/Navbar.vue";
import { fetchJson } from "../utils/api";

const loading = ref(false);
const error = ref("");
const studyStats = ref({});
const participantStats = ref({});
const literatureStats = ref({});

const loadStats = async () => {
  loading.value = true;
  error.value = "";
  try {
    const [studies, participants, literature] = await Promise.all([
      fetchJson("/studies/stats/"),
      fetchJson("/participants/stats/"),
      fetchJson("/literature/stats/"),
    ]);
    studyStats.value = studies;
    participantStats.value = participants;
    literatureStats.value = literature;
  } catch (err) {
    error.value = err.message || "Failed to load statistics";
  } finally {
    loading.value = false;
  }
};

onMounted(loadStats);
</script>
