<template>
    <div>
        Select server:
        <select :value="modelValue" @change="onChange">
        <option v-if="!servers.length" disabled>Loading...</option>
        <option v-for="server in servers" :key="server.ID ?? server.id ?? server.Servername" :value="server.Servername">
            {{ server.Servername }}
        </option>
        </select>
    </div>
</template>

<script setup>
    defineProps({
        modelValue: {
            type: [String, Number],
            default: ''
        },
        servers: {
            type: Array,    
            default: () => []
        }
    });
    const emit = defineEmits(['update:modelValue', 'change']);

    function onChange(event) {
        const value = event.target.value;
        emit('update:modelValue', value);
        emit('change', value);
    }
</script>