<template>
    <div>
        <div>
            Select server:
            <select v-model="selectedServer" @change="onServerChange">
                <option v-if="!servers.length" disabled>Loading...</option>
                <option v-for="server in servers" :key="server.ID ?? server.id ?? server.Servername" :value="server.Servername">{{ server.Servername }}</option>
            </select>
        </div>
        
        <div v-if="!logData.length">Geen loggegevens beschikbaar</div>
        <table v-else class="log-table">
            <thead>
                <tr>
                    <th v-for="column in columns" :key="column">{{ column }}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(log, index) in logData" :key="index">
                    <td v-for="column in columns" :key="column">
                        {{ formatCell(log[column]) }}
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="pagination" v-if="totalPages > 1">
            <submit-button @click="goToPage(currentPage - 1)" :disabled="currentPage <= 1">Vorige</submit-button>
            <submit-button
              v-for="p in pageNumbers"
              :key="p"
              @click="goToPage(p)"
              :class="{ active: p === currentPage }"
            >{{ p }}</submit-button>
            <submit-button @click="goToPage(currentPage + 1)" :disabled="currentPage >= totalPages">Volgende</submit-button>
            <div>
                <span class="page-info">Pagina {{ currentPage }} van {{ totalPages }} ({{ total }} records)</span>
            </div>
            <label>
                Per pagina:
                <select v-model.number="limit" @change="changeLimit">
                    <option :value="10">10</option>
                    <option :value="25">25</option>
                    <option :value="50">50</option>
                </select>
            </label>
        </div>
    </div>
</template>

<script setup>
import SubmitButton from '../ui/SubmitButton.vue';
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';

const store = useStore();
const logData = ref([]);
const url = 'http://' + process.env.VUE_APP_apiserver + '/api/v1/logging';

const authToken = computed(function () {
    return store.getters.getAuthToken;
});

// pagination state
const currentPage = ref(1);
const limit = ref(10);
const total = ref(0);
const totalPages = ref(0);

// servers for select
const servers = ref([]);
const selectedServer = ref('');

async function fetchServers() {
    try {
        const response = await axios.get('http://' + process.env.VUE_APP_apiserver + '/api/v1/server', {
          headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authentication': 'Bearer ' + authToken.value
          }
        });
        const payload = response.data;
        servers.value = Array.isArray(payload) ? payload : (payload && payload.data ? payload.data : []);
        // set default selected server if none selected
        if (!selectedServer.value && servers.value.length) {
            // prefer Servername field, fallback to first item string
            selectedServer.value = servers.value[0].Servername ?? servers.value[0].name ?? servers.value[0];
        }
    } catch (error) {
        console.error('Error fetching servers:', error);
    }
}

const responseData = async (page = 1, useServer = false) => {
    try {
        // build endpoint: use /api/v1/logging/{serverName} only when useServer is true
        const endpoint = useServer && selectedServer.value
            ? `${url}/${encodeURIComponent(selectedServer.value)}`
            : url;

        const response = await axios.get(endpoint, {
            params: { page: page, limit: limit.value },
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
                'Authentication': 'Bearer ' + authToken.value
            }
        });

        const payload = response.data;
        const rows = Array.isArray(payload) ? payload : (payload && payload.data ? payload.data : []);
        logData.value = rows;

        if (payload && typeof payload === 'object') {
            currentPage.value = payload.page ?? page;
            limit.value = payload.limit ?? limit.value;
            total.value = payload.total ?? total.value;
            totalPages.value = payload.totalPages ?? (payload.total && limit.value ? Math.ceil(payload.total / limit.value) : totalPages.value);
        }

        if (!totalPages.value && total.value && limit.value) {
            totalPages.value = Math.ceil(total.value / limit.value);
        }
    } catch (error) {
        console.error('Error fetching log data:', error);
    }
};

const columns = computed(() => {
    return logData.value.length > 0 ? Object.keys(logData.value[0]) : [];
});

const formatCell = (val) => {
    if (val === null || val === undefined) return '';
    if (typeof val === 'object') return JSON.stringify(val);
    return String(val);
}

onMounted(async () => {
  // populate the select box first
  await fetchServers();
  // initial load: show ALL records (do not filter by server)
  responseData(1, false);
});

const pageNumbers = computed(() => {
    const pages = [];
    const totalP = Math.max(1, totalPages.value || 1);
    const start = Math.max(1, currentPage.value - 3);
    const end = Math.min(totalP, currentPage.value + 3);
    for (let p = start; p <= end; p++) pages.push(p)
    return pages;
});

function goToPage(p) {
    if (p < 1) p = 1;
    if (totalPages.value && p > totalPages.value) p = totalPages.value;
    if (p === currentPage.value) return;
    currentPage.value = p;
    // if a server is selected, keep filtering while paging
    responseData(p, !!selectedServer.value);
}

function changeLimit() {
    currentPage.value = 1;
    responseData(1, !!selectedServer.value);
}

function onServerChange() {
    currentPage.value = 1;
    // when user changes selection, fetch only that server's logs
    responseData(1, true);
}
</script>

<style>
.log-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0.5rem;
}
.log-table th,
.log-table td {
  border: 1px solid #ddd;
  padding: 0.5rem;
  text-align: left;
  font-family: monospace;
  font-size: 0.9rem;
}
.log-table thead {
  background: #f5f5f5;
}

.pagination {
  justify-content: center;
  margin-top: 0.75rem;
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
}
.pagination button {
  padding: 0.25rem 0.5rem;
}
.pagination button.active {
  font-weight: bold;
  background: #eee;
}
.page-info {
  margin-left: 0.5rem;
  font-size: 0.9rem;
}
</style>