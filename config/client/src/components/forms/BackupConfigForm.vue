<template>
    <form action="#" id="form" class="config-form grid grid-cols-2 gap-4">
        <!-- <div class="grid grid-flow-row grid-cols-2 gap-4"></div> -->
        <div class="config-form-fields">
            <div class=""><label for="filetype" class="config-form-label w-fit">filetype</label></div>
            <div class=""><input type="text" v-model="filetype" name="filetype" id="filetype" class="input-border config-form-input"></div>
        </div>
        <div class="config-form-col2 config-form-fields">
            <label for="backuppath" class="config-form-label w-fit">Backuppath</label>
            <input type="text" v-model="backuppath" name="backuppath" id="backuppath" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="logfilepath" class="config-form-label w-fit">logfilepath</label>
            <input type="text" v-model="logfilepath" name="logfilepath" id="logfilepath" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="scriptspath" class="config-form-label w-fit">scriptspath</label>
            <input type="text" v-model="scriptspath" name="scriptspath" id="scriptspath" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="apiurl" class="config-form-label w-fit">apiurl</label>
            <input type="text" v-model="apiurl" name="apiurl" id="apiurl" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="sourcesLocation" class="config-form-label w-fit">sourcesLocation</label>
            <input type="text" v-model="sourcesLocation" name="sourcesLocation" id="sourcesLocation" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="compression" class="config-form-label w-fit">compression</label>
            <input type="text" v-model="compression" name="compression" id="compression" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">    
            <label for="backupserver" class="config-form-label w-fit">backupserver</label>
            <input type="text" v-model="backupserver" name="backupserver" id="backupserver" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="copycommand" class="config-form-label w-fit">copycommand</label>
            <input type="text" v-model="copycommand" name="copycommand" id="copycommand" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="remotefilepath" class="config-form-label w-fit">remotefilepath</label>
            <input type="text" v-model="remotefilepath" name="remotefilepath" id="remotefilepath" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="mailserver" class="config-form-label w-fit">mailserver</label>
            <input type="text" v-model="mailserver" name="mailserver" id="mailserver" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="mailRecipient" class="config-form-label w-fit">mailRecipient</label>
            <input type="text" v-model="mailRecipient" name="mailRecipient" id="mailRecipient" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="mailSender" class="config-form-label w-fit">mailSender</label>
            <input type="text" v-model="mailSender" name="mailSender" id="mailSender" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="debug" class="config-form-label w-fit">debug</label>
            <input type="text" v-model="debug" name="debug" id="debug" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="hostType" class="config-form-label w-fit">hostType</label>
            <input type="text" v-model="hostType" name="hostType" id="hostType" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="timerUnits" class="config-form-label w-fit">timerUnits</label>
            <input type="text" v-model="timerUnits" name="timerUnits" id="timerUnits" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="servicesToInstall" class="config-form-label w-fit">servicesToInstall</label>
            <input type="text" v-model="servicesToInstall" name="servicesToInstall" id="servicesToInstall" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="servicesToCopy" class="config-form-label w-fit">servicesToCopy</label>
            <input type="text" v-model="servicesToCopy" name="servicesToCopy" id="servicesToCopy" class="input-border config-form-input">
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
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const store = useStore()
const filetype = ref('');
const backuppath = ref('');
const logfilepath = ref('');
const scriptspath = ref('');
const apiurl = ref('');
const sourcesLocation = ref('');
const compression = ref('');
const backupserver = ref('');
const copycommand = ref('');
const remotefilepath = ref('');
const mailserver = ref('');
const mailRecipient = ref('');
const mailSender = ref('');
const debug = ref('');
const hostType = ref('');
const timerUnits = ref('');
const servicesToInstall = ref('');
const servicesToCopy = ref('');


const authToken = computed(function () {
    return store.getters.getAuthToken;
})

console.log(authToken);

async function submitConfigForm() {
    if (authToken.value) {
        console.log("niet leeg, submitting")
        const response = await axios.put('http://127.0.0.1:8081/api/v1/configuration', {
            filetype: filetype.value,
            backuppath: backuppathfiletype.value,
            logfilepath: logfilepathfiletype.value,
            scriptspath: scriptspathfiletype.value,
            apiurl: apiurlfiletype.value,
            sourcesLocation: sourcesLocationfiletype.value,
            compression: compressionfiletype.value,
            backupserver: backupserverfiletype.value,
            copycommand: copycommandfiletype.value,
            remotefilepath: remotefilepathfiletype.value,
            mailserver: mailserverfiletype.value,
            mailRecipient: mailRecipientfiletype.value,
            mailSender: mailSenderfiletype.value,
            debug: debugfiletype.value,
            hostType: hostTypefiletype.value,
            timerUnits: timerUnitsfiletype.value,
            servicesToInstall: servicesToInstallfiletype.value,
            servicesToCopy: servicesToCopy.value
        }, {
            headers: {
                'Content-Type': 'application/json; charset=UTF-8',
                'Authentication': 'Bearer ' + authToken.value
                // bearer token
            },
        });

        if (response.ok) {
            console.log("opgeslagen");
        }
    }
}

onMounted( async () => {
    if (authToken.value) {
        try {
            const response = await axios.get('http://127.0.0.1:8081/api/v1/configuration', {
                headers: {
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Authentication': 'Bearer ' + authToken.value
                }
            });

            if (response.status == 200) {
                console.log(response.data);
                filetype.value = response.data.filetype
                backuppath.value = response.data.backuppath
                logfilepath.value = response.data.logfilepath
                scriptspath.value = response.data.scriptspath
                apiurl.value= response.data.apiurl
                sourcesLocation.value = response.data.sourcesLocation
                compression.value = response.data.compression
                backupserver.value = response.data.backupserver
                copycommand.value = response.data.copycommand
                remotefilepath.value = response.data.remotefilepath
                mailserver.value = response.data.mailserver
                mailRecipient.value = response.data.mailRecipient
                mailSender.value = response.data.mailSender
                debug.value = response.data.debug
                hostType.value = response.data.hostType
                timerUnits.value = response.data.timerUnits
                servicesToInstall.value = response.data.servicesToInstall
                servicesToCopy.value = response.data.servicesToCopy
            }
        } catch (error) {
            console.log(error);
        }

    }
}) 

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