<template>
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
            <select v-model.number="localLimit">
                <option :value="10">10</option>
                <option :value="25">25</option>
                <option :value="50">50</option>
            </select>
        </label>
    </div>
</template>
<script setup>
// import UI components
import SubmitButton from './SubmitButton.vue';

import { computed } from 'vue';
const localLimit = computed({
    get() {
        return props.limit;
    },
    set(value) {
        emit('change-limit', Number(value));
    }
});

const props = defineProps({
    currentPage: {
        type: Number,
        required: true
    },
    totalPages: {
        type: Number,
        required: true
    },
    total: {
        type: Number,
        default: 0
    },
    limit: {
        type: Number,
        default: 10
    },
    pageNumbers: {
        type: Array,
        default: () => []
    }
});

const emit = defineEmits(['change-page', 'change-limit']);

function goToPage(page) {
    if (page < 1) page = 1;
    // props are available in template; runtime check:
    // contstrain by totalPages prop if provided
    emit('change-page', page);
}
</script>
<style scoped>
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