<template>
  <div>
    <div v-if="!rows || !rows.length">Geen loggegevens beschikbaar</div>
    <table v-else class="log-table">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col">{{ col }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rIdx) in rows" :key="rIdx">
          <td v-for="col in columns" :key="col">{{ formatCell(row[col]) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  rows: { type: Array, default: () => [] },
  columns: { type: Array, default: () => [] }
});

function formatCell(val) {
  if (val === null || val === undefined) return '';
  if (typeof val === 'object') return JSON.stringify(val);
  return String(val);
}
</script>

<style scoped>
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