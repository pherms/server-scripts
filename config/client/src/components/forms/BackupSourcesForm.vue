<template>
  <div class="layout">
    <form action="#" id="form">
        <label for="sources" class="input-form-label">Sources om te backuppen</label>
        <textarea v-model="sourcesInput" name="sources" id="sources" cols="30" rows="10" class="config-form-fields input-border config-form-input w-fit"></textarea>
    </form>
    <submit-button @click="submitSourcesForm">Opslaan</submit-button>
  </div>
</template>
<script setup>
import SubmitButton from '../ui/SubmitButton.vue'
import { ref, onMounted, computed, inject } from 'vue'
import { useStore } from 'vuex'
import axios from 'axios'

const sourcesInput = ref({})
const apiServer = inject('apiServer');

const store = useStore();
const url = 'http://' + apiServer + '/api/v1/sources';

const authToken = computed(function () {
    return store.getters.getAuthToken;
});

const responseData = async () => {
    try {
        const response = await axios.get(url, {
          headers: {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authentication': 'Bearer ' + authToken.value
          }
        });
        sourcesInput.value = response.data.sources;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

async function submitSourcesForm() {
    if (authToken.value) {
        console.log("niet leeg, submitting")
        try {
          const response = await axios.post(url,
            {
              data: {
                sources: sourcesInput.value
              }
            }
          , {
              headers: {
                  'Content-Type': 'application/json; charset=UTF-8',
                  'Authentication': 'Bearer ' + authToken.value
              },
          });

          if (response.status === 201) {
              console.log("opgeslagen");
          }
        } catch (error) {
            console.log('Something went wrong:', error);
        }


    }
}
onMounted(() => {
  responseData();
});

</script>

<style scoped>
.input-border {
  border-color: #1E0342;
  border: solid 1px;
  border-radius: 5px;
  padding: 0.4rem;
}

.config-form-input {
  line-height: 32px;
  font-size: 18px;
  color: #1E0342;
  margin: 1rem 1rem;
}

.config-form-fields {
  display: flex;
  justify-content: space-between;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
  padding-left: 1rem;
}

.config-form-label {
  position: relative;
  margin-bottom: 1rem;
}

.w-fit {
  width: -moz-fit-content;
  width: fit-content;
}

.layout {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>