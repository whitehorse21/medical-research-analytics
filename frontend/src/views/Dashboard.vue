<template>
  <div class="dashboard">
    <Navbar />
    <div class="dashboard-content">
      <div class="dashboard-header">
        <div>
          <h1>Research Analytics Dashboard</h1>
          <p class="subtitle">Comprehensive overview of your medical research platform</p>
        </div>
        <button @click="loadStats" class="refresh-btn" :disabled="loading">
          <span v-if="!loading">↻ Refresh</span>
          <span v-else>Loading...</span>
        </button>
      </div>

      <div v-if="loading" class="loading-container">
        <div class="spinner"></div>
        <p>Loading analytics...</p>
      </div>
      <div v-if="error" class="error-banner">{{ error }}</div>
      
      <div v-if="!loading && !error" class="dashboard-grid">
        <!-- Key Metrics Row -->
        <div class="metrics-row">
          <div class="metric-card primary">
            <div class="metric-icon">📊</div>
            <div class="metric-content">
              <div class="metric-label">Total Studies</div>
              <div class="metric-value">{{ studyStats.total_studies || 0 }}</div>
              <div class="metric-change">
                <span class="change-positive">+{{ studyStats.recent_studies || 0 }}</span>
                <span class="change-label">new this month</span>
              </div>
            </div>
          </div>

          <div class="metric-card success">
            <div class="metric-icon">👥</div>
            <div class="metric-content">
              <div class="metric-label">Total Participants</div>
              <div class="metric-value">{{ participantStats.total_participants || 0 }}</div>
              <div class="metric-change">
                <span class="change-positive">+{{ participantStats.recent_enrollments || 0 }}</span>
                <span class="change-label">enrolled this month</span>
              </div>
            </div>
          </div>

          <div class="metric-card info">
            <div class="metric-icon">📚</div>
            <div class="metric-content">
              <div class="metric-label">Literature Articles</div>
              <div class="metric-value">{{ literatureStats.total_articles || 0 }}</div>
              <div class="metric-change">
                <span class="change-positive">+{{ literatureStats.recent_articles || 0 }}</span>
                <span class="change-label">added this month</span>
              </div>
            </div>
          </div>

          <div class="metric-card warning">
            <div class="metric-icon">✅</div>
            <div class="metric-content">
              <div class="metric-label">Completion Rate</div>
              <div class="metric-value">{{ studyStats.completion_rate || 0 }}%</div>
              <div class="metric-change">
                <span>{{ studyStats.completed_studies || 0 }} of {{ studyStats.total_studies || 0 }}</span>
                <span class="change-label">studies completed</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Studies Analytics -->
        <div class="analytics-card">
          <div class="card-header">
            <h2>Studies Overview</h2>
            <router-link to="/studies" class="view-all-link">View All →</router-link>
          </div>
          <div class="card-body">
            <div class="stats-grid-2">
              <div class="stat-section">
                <div class="stat-title">Status Distribution</div>
                <div class="status-list">
                  <div v-for="(count, status) in studyStats.by_status" :key="status" class="status-item">
                    <div class="status-info">
                      <span class="status-name">{{ status.charAt(0).toUpperCase() + status.slice(1) }}</span>
                      <span class="status-count">{{ count }}</span>
                    </div>
                    <div class="progress-bar">
                      <div 
                        class="progress-fill" 
                        :class="`status-${status}`"
                        :style="{ width: `${(count / (studyStats.total_studies || 1)) * 100}%` }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="stat-section">
                <div class="stat-title">Key Metrics</div>
                <div class="metric-list">
                  <div class="metric-item">
                    <span class="metric-name">Active Studies</span>
                    <span class="metric-number highlight">{{ studyStats.active_studies || 0 }}</span>
                  </div>
                  <div class="metric-item">
                    <span class="metric-name">Ongoing Studies</span>
                    <span class="metric-number">{{ studyStats.ongoing_studies || 0 }}</span>
                  </div>
                  <div class="metric-item">
                    <span class="metric-name">Studies with Dates</span>
                    <span class="metric-number">{{ studyStats.studies_with_dates || 0 }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Participants Analytics -->
        <div class="analytics-card">
          <div class="card-header">
            <h2>Participants Analytics</h2>
            <router-link to="/participants" class="view-all-link">View All →</router-link>
          </div>
          <div class="card-body">
            <div class="stats-grid-2">
              <div class="stat-section">
                <div class="stat-title">Demographics</div>
                <div class="demographic-stats">
                  <div class="demo-item">
                    <span class="demo-label">Average Age</span>
                    <span class="demo-value">{{ participantStats.average_age || 0 }} years</span>
                  </div>
                  <div class="demo-item">
                    <span class="demo-label">Age Range</span>
                    <span class="demo-value">{{ participantStats.min_age || 0 }} - {{ participantStats.max_age || 0 }} years</span>
                  </div>
                  <div class="demo-item">
                    <span class="demo-label">Avg per Study</span>
                    <span class="demo-value">{{ participantStats.average_per_study || 0 }}</span>
                  </div>
                </div>
                <div class="gender-distribution">
                  <div v-for="(count, sex) in participantStats.by_sex" :key="sex" class="gender-item">
                    <div class="gender-bar">
                      <div 
                        class="gender-fill" 
                        :style="{ width: `${(count / (participantStats.total_participants || 1)) * 100}%` }"
                      ></div>
                    </div>
                    <div class="gender-info">
                      <span class="gender-label">{{ sex }}</span>
                      <span class="gender-count">{{ count }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="stat-section">
                <div class="stat-title">Age Groups</div>
                <div class="age-groups">
                  <div v-for="(count, group) in participantStats.age_groups" :key="group" class="age-group-item">
                    <div class="age-group-header">
                      <span class="age-group-label">{{ group }} years</span>
                      <span class="age-group-count">{{ count }}</span>
                    </div>
                    <div class="progress-bar">
                      <div 
                        class="progress-fill age-fill"
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
        <div class="analytics-card">
          <div class="card-header">
            <h2>Literature Repository</h2>
            <router-link to="/literature" class="view-all-link">View All →</router-link>
          </div>
          <div class="card-body">
            <div class="stats-grid-2">
              <div class="stat-section">
                <div class="stat-title">Publication Trends</div>
                <div class="trend-stats">
                  <div class="trend-item">
                    <span class="trend-label">Current Year ({{ new Date().getFullYear() }})</span>
                    <span class="trend-value">{{ literatureStats.current_year_articles || 0 }}</span>
                  </div>
                  <div class="trend-item">
                    <span class="trend-label">Last Year ({{ new Date().getFullYear() - 1 }})</span>
                    <span class="trend-value">{{ literatureStats.last_year_articles || 0 }}</span>
                  </div>
                  <div class="trend-item">
                    <span class="trend-label">DOI Coverage</span>
                    <span class="trend-value">{{ literatureStats.doi_coverage || 0 }}%</span>
                  </div>
                </div>
                <div v-if="literatureStats.year_range" class="year-range">
                  <span class="range-label">Publication Range:</span>
                  <span class="range-value">{{ literatureStats.year_range.min_year || 'N/A' }} - {{ literatureStats.year_range.max_year || 'N/A' }}</span>
                </div>
              </div>
              <div class="stat-section">
                <div class="stat-title">Top Journals</div>
                <div class="journals-list">
                  <div 
                    v-for="(journal, index) in (literatureStats.top_journals || []).slice(0, 5)" 
                    :key="index" 
                    class="journal-item"
                  >
                    <div class="journal-rank">{{ index + 1 }}</div>
                    <div class="journal-info">
                      <span class="journal-name">{{ journal.journal }}</span>
                      <span class="journal-count">{{ journal.count }} articles</span>
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

<style scoped>
.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  overflow-x: hidden;
  width: 100%;
}

.dashboard-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
  box-sizing: border-box;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.dashboard-header h1 {
  margin: 0 0 0.5rem 0;
  color: #1a202c;
  font-size: 2.5rem;
  font-weight: 700;
  word-wrap: break-word;
  line-height: 1.2;
}

.subtitle {
  color: #718096;
  font-size: 1.1rem;
  margin: 0;
}

.refresh-btn {
  background: white;
  border: 2px solid #667eea;
  color: #667eea;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: #667eea;
  color: white;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

.error-banner {
  background: #fed7d7;
  color: #c53030;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 500;
}

.dashboard-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.metrics-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.metric-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.metric-card.primary { border-left: 4px solid #667eea; }
.metric-card.success { border-left: 4px solid #48bb78; }
.metric-card.info { border-left: 4px solid #4299e1; }
.metric-card.warning { border-left: 4px solid #ed8936; }

.metric-icon {
  font-size: 2.5rem;
}

.metric-content {
  flex: 1;
}

.metric-label {
  color: #718096;
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric-value {
  color: #1a202c;
  font-size: 2rem;
  font-weight: 700;
  margin: 0.5rem 0;
}

.metric-change {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.change-positive {
  color: #48bb78;
  font-weight: 600;
}

.change-label {
  color: #a0aec0;
}

.analytics-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.card-header h2 {
  margin: 0;
  color: #1a202c;
  font-size: 1.5rem;
  font-weight: 600;
}

.view-all-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.view-all-link:hover {
  color: #5568d3;
}

.card-body {
  padding: 1.5rem;
}

.stats-grid-2 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  width: 100%;
}

.stat-title {
  color: #4a5568;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.status-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.status-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-name {
  color: #4a5568;
  font-weight: 500;
  text-transform: capitalize;
}

.status-count {
  color: #1a202c;
  font-weight: 600;
}

.progress-bar {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s;
}

.progress-fill.status-planning { background: #fbbf24; }
.progress-fill.status-recruiting { background: #3b82f6; }
.progress-fill.status-active { background: #10b981; }
.progress-fill.status-completed { background: #6366f1; }
.progress-fill.status-cancelled { background: #ef4444; }
.progress-fill.age-fill { background: #667eea; }

.metric-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.metric-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f7fafc;
  border-radius: 8px;
}

.metric-name {
  color: #718096;
  font-size: 0.875rem;
}

.metric-number {
  color: #1a202c;
  font-weight: 600;
  font-size: 1.125rem;
}

.metric-number.highlight {
  color: #667eea;
  font-size: 1.25rem;
}

.demographic-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.demo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f7fafc;
  border-radius: 8px;
}

.demo-label {
  color: #718096;
  font-size: 0.875rem;
}

.demo-value {
  color: #1a202c;
  font-weight: 600;
}

.gender-distribution {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.gender-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.gender-bar {
  height: 24px;
  background: #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
}

.gender-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  transition: width 0.3s;
}

.gender-info {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
}

.gender-label {
  color: #4a5568;
  font-weight: 500;
}

.gender-count {
  color: #1a202c;
  font-weight: 600;
}

.age-groups {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.age-group-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.age-group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.age-group-label {
  color: #4a5568;
  font-weight: 500;
  font-size: 0.875rem;
}

.age-group-count {
  color: #1a202c;
  font-weight: 600;
}

.trend-stats {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.trend-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f7fafc;
  border-radius: 8px;
}

.trend-label {
  color: #718096;
  font-size: 0.875rem;
}

.trend-value {
  color: #1a202c;
  font-weight: 600;
  font-size: 1.125rem;
}

.year-range {
  padding: 1rem;
  background: #edf2f7;
  border-radius: 8px;
  text-align: center;
}

.range-label {
  color: #718096;
  font-size: 0.875rem;
  margin-right: 0.5rem;
}

.range-value {
  color: #1a202c;
  font-weight: 600;
}

.journals-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.journal-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: #f7fafc;
  border-radius: 8px;
  transition: background 0.2s;
}

.journal-item:hover {
  background: #edf2f7;
}

.journal-rank {
  width: 32px;
  height: 32px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.journal-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.journal-name {
  color: #1a202c;
  font-weight: 500;
  font-size: 0.875rem;
}

.journal-count {
  color: #718096;
  font-size: 0.75rem;
}

@media (max-width: 1200px) {
  .dashboard-content {
    padding: 1.5rem;
  }
}

@media (max-width: 1024px) {
  .dashboard-content {
    padding: 1.5rem;
  }

  .dashboard-header h1 {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .metrics-row {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.25rem;
  }

  .stats-grid-2 {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .dashboard-content {
    padding: 1rem;
  }

  .dashboard-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  .dashboard-header h1 {
    font-size: 1.5rem;
    line-height: 1.3;
  }

  .subtitle {
    font-size: 0.875rem;
  }

  .refresh-btn {
    width: 100%;
    justify-content: center;
    min-height: 44px;
  }

  .metrics-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .metric-card {
    padding: 1.5rem;
    width: 100%;
  }

  .metric-value {
    font-size: 2.5rem;
  }

  .analytics-card {
    padding: 1.5rem;
    width: 100%;
  }

  .card-body {
    padding: 1.5rem;
    padding-top: 20px !important;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    flex-wrap: wrap;
  }

  .card-header h2 {
    font-size: 1.25rem;
    word-wrap: break-word;
  }

  .status-list,
  .demographics-list,
  .gender-distribution,
  .age-groups {
    gap: 0.75rem;
    padding-top: 20px;
  }

  .status-item,
  .demographic-item {
    padding: 0.75rem;
  }

  .stat-section {
    padding: 1rem 0;
  }
}

@media (max-width: 480px) {
  .dashboard-content {
    padding: 0.75rem;
  }

  .dashboard-header {
    margin-bottom: 1rem;
  }

  .dashboard-header h1 {
    font-size: 1.25rem;
    line-height: 1.2;
  }

  .subtitle {
    font-size: 0.8rem;
  }

  .metric-card {
    padding: 1rem;
  }

  .metric-icon {
    font-size: 2rem;
  }

  .metric-value {
    font-size: 2rem;
  }

  .metric-label {
    font-size: 0.875rem;
  }

  .metric-change {
    font-size: 0.8rem;
  }

  .analytics-card {
    padding: 1rem;
  }

  .card-body {
    padding: 1rem;
    padding-top: 20px !important;
  }

  .card-header h2 {
    font-size: 1.125rem;
  }

  .stat-title {
    font-size: 0.875rem;
  }

  .status-name,
  .demographic-label {
    font-size: 0.875rem;
  }

  .status-count,
  .demographic-count {
    font-size: 0.875rem;
  }

  .journal-name {
    font-size: 0.8rem;
  }

  .journal-count {
    font-size: 0.75rem;
  }

  .status-list,
  .demographics-list,
  .gender-distribution,
  .age-groups {
    padding-top: 20px;
  }
}
</style>
