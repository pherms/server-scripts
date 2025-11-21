<template>
    <form action="#" id="form" class="config-form grid grid-cols-2 gap-4">
        <!-- <div class="grid grid-flow-row grid-cols-2 gap-4"></div> -->
        <div class="config-form-fields">
            <label for="filetype" class="config-form-label w-fit">filetype</label>
            <input type="text" v-model="form.filetype" name="filetype" id="filetype" class="input-border config-form-input">
        </div>
        <div class="config-form-col2 config-form-fields">
            <label for="backuppath" class="config-form-label w-fit">Backuppath</label>
            <input type="text" v-model="form.backuppath" name="backuppath" id="backuppath" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="logfilepath" class="config-form-label w-fit">logfilepath</label>
            <input type="text" v-model="form.logfilepath" name="logfilepath" id="logfilepath" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="scriptspath" class="config-form-label w-fit">scriptspath</label>
            <input type="text" v-model="form.scriptspath" name="scriptspath" id="scriptspath" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="apiurl" class="config-form-label w-fit">apiurl</label>
            <input type="text" v-model="form.apiurl" name="apiurl" id="apiurl" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="sourcesLocation" class="config-form-label w-fit">sourcesLocation</label>
            <input type="text" v-model="form.sourcesLocation" name="sourcesLocation" id="sourcesLocation" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="compression" class="config-form-label w-fit">compression</label>
            <input type="text" v-model="form.compression" name="compression" id="compression" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">    
            <label for="backupserver" class="config-form-label w-fit">backupserver</label>
            <input type="text" v-model="form.backupserver" name="backupserver" id="backupserver" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="copycommand" class="config-form-label w-fit">copycommand</label>
            <input type="text" v-model="form.copycommand" name="copycommand" id="copycommand" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="remotefilepath" class="config-form-label w-fit">remotefilepath</label>
            <input type="text" v-model="form.remotefilepath" name="remotefilepath" id="remotefilepath" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="mailserver" class="config-form-label w-fit">mailserver</label>
            <input type="text" v-model="form.mailserver" name="mailserver" id="mailserver" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="mailRecipient" class="config-form-label w-fit">mailRecipient</label>
            <input type="text" v-model="form.mailRecipient" name="mailRecipient" id="mailRecipient" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="mailSender" class="config-form-label w-fit">mailSender</label>
            <input type="text" v-model="form.mailSender" name="mailSender" id="mailSender" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="debug" class="config-form-label w-fit">debug</label>
            <input type="text" v-model="form.debug" name="debug" id="debug" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="hostType" class="config-form-label w-fit">hostType</label>
            <input type="text" v-model="form.hostType" name="hostType" id="hostType" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="timerUnits" class="config-form-label w-fit">timerUnits</label>
            <input type="text" v-model="form.timerUnits" name="timerUnits" id="timerUnits" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="servicesToInstall" class="config-form-label w-fit">servicesToInstall</label>
            <input type="text" v-model="form.servicesToInstall" name="servicesToInstall" id="servicesToInstall" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="servicesToCopy" class="config-form-label w-fit">servicesToCopy</label>
            <input type="text" v-model="form.servicesToCopy" name="servicesToCopy" id="servicesToCopy" class="input-border config-form-input">
        </div>
 
        <div class="config-form-fields">
            <!-- <button id="submit" class="button">Save data</button> -->
            <submit-button @click="submitConfigForm">Opslaan</submit-button>
        </div>
    </form>  
</template>
<script setup>
import SubmitButton from '../ui/SubmitButton.vue';
import { useStore } from 'vuex';
import { ref, computed, onMounted, inject } from 'vue';
import axios from 'axios';

const form = ref({});
const apiServer = inject('apiServer');

const store = useStore();
const url = 'http://' + apiServer + '/api/v1/configuration';

const authToken = computed(function () {
    return store.getters.getAuthToken;
});

console.log(authToken.value);

const responseData = async () => {
    try {
        await axios.get(url, {
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
                'Authentication': 'Bearer ' + authToken.value
            }
        }).then(response => {
            form.value = response.data;
        });
        console.log(form.value);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

async function submitConfigForm() {
    if (authToken.value) {
        console.log("niet leeg, submitting")
        await axios.post(url,
            {
                data: form.value
            },
            {
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Authentication': 'Bearer ' + authToken.value
                    // bearer token
                },
        })
        .then((response) => {
            if (response.status === 201) {
                console.log('opgeslagen');
            }
        })
        .catch((error) => {
            console.log(error);
        });
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
  line-height: 32px;
  font-size: 18px;
  color: #1E0342;
}

.input-border:focus {
    border-color: #0E46A3;
}

.config-form {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.25rem;
}

.config-form-col2 {
  grid-column-start: 2;
}

.config-form-input {
  position: relative;
  width: 20rem;
}

.config-form-fields {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
  padding-left: 1rem;
}

.config-form-label {
  position: relative;
  margin-right: 1rem;
}

.w-fit {
  width: -moz-fit-content;
  width: fit-content;
}
</style>