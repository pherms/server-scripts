<template>
    <div>
        <server-select v-model="selectedServer" :servers="servers" @change="onServerChange" />

        <logview-table :rows="logData" :columns="columns" />
        <data-pagination
            :current-page="currentPage"
            :total-pages="totalPages"
            :total="total"
            :limit="limit"
            :page-numbers="pageNumbers"
            @change-page="goToPage"
            @change-limit="onChangeLimit"
        />
    </div>
</template>

<script setup>
// import UI components
import ServerSelect from '../ui/SelectBox.vue';
import LogviewTable from '../ui/LogviewTable.vue';
import DataPagination from '../ui/DataPagination.vue';

import { ref, onMounted, computed, inject } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';

const store = useStore();
const logData = ref([]);
const apiServer = inject('apiServer');
    
const url = 'http://' + apiServer + '/api/v1/logging';

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
const filterByServer = ref(false);

async function fetchServers() {
    try {
        const response = await axios.get('http://' + apiServer + '/api/v1/server', {
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
        console.error('fetching servers failed');
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
        console.error('responseData failed');
    }
};

const columns = computed(() => {
    return logData.value.length > 0 ? Object.keys(logData.value[0]) : [];
});

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
    responseData(p, filterByServer.value);
}

function onChangeLimit(newLimit) {
    limit.value = newLimit;
    // reset to first page and fetch current filter state
    currentPage.value = 1;
    responseData(1, filterByServer.value);
}

function onServerChange() {
    currentPage.value = 1;
    // user explicitly changed server selection
    filterByServer.value = true;
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
</style>