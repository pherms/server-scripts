<template>
    <form action="#" id="form" class="config-form grid grid-cols-2 gap-4">
        <!-- <div class="grid grid-flow-row grid-cols-2 gap-4"></div> -->
        <div class="config-form-fields">
            <div class=""><label for="filetype" class="config-form-label w-fit">filetype</label></div>
            <div class=""><input type="text" name="filetype" id="filetype" class="input-border config-form-input"></div>
        </div>
        <div class="config-form-col2 config-form-fields">
            <label for="backuppath" class="config-form-label w-fit">Backuppath</label>
            <input type="text" name="backuppath" id="backuppath" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="logfilepath" class="config-form-label w-fit">logfilepath</label>
            <input type="text" name="logfilepath" id="logfilepath" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="scriptspath" class="config-form-label w-fit">scriptspath</label>
            <input type="text" name="scriptspath" id="scriptspath" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="apiurl" class="config-form-label w-fit">apiurl</label>
            <input type="text" name="apiurl" id="apiurl" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="sourcesLocation" class="config-form-label w-fit">sourcesLocation</label>
            <input type="text" name="sourcesLocation" id="sourcesLocation" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="compression" class="config-form-label w-fit">compression</label>
            <input type="text" name="compression" id="compression" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">    
            <label for="backupserver" class="config-form-label w-fit">backupserver</label>
            <input type="text" name="backupserver" id="backupserver" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="copycommand" class="config-form-label w-fit">copycommand</label>
            <input type="text" name="copycommand" id="copycommand" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="remotefilepath" class="config-form-label w-fit">remotefilepath</label>
            <input type="text" name="remotefilepath" id="remotefilepath" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="mailserver" class="config-form-label w-fit">mailserver</label>
            <input type="text" name="mailserver" id="mailserver" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="mailRecipient" class="config-form-label w-fit">mailRecipient</label>
            <input type="text" name="mailRecipient" id="mailRecipient" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="mailSender" class="config-form-label w-fit">mailSender</label>
            <input type="text" name="mailSender" id="mailSender" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="debug" class="config-form-label w-fit">debug</label>
            <input type="text" name="debug" id="debug" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="hostType" class="config-form-label w-fit">hostType</label>
            <input type="text" name="hostType" id="hostType" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="timerUnits" class="config-form-label w-fit">timerUnits</label>
            <input type="text" name="timerUnits" id="timerUnits" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="servicesToInstall" class="config-form-label w-fit">servicesToInstall</label>
            <input type="text" name="servicesToInstall" id="servicesToInstall" class="input-border config-form-input">
        </div>
        <div class="config-form-fields">
            <label for="servicesToCopy" class="config-form-label w-fit">servicesToCopy</label>
            <input type="text" name="servicesToCopy" id="servicesToCopy" class="input-border config-form-input">
        </div>
    
    <div class="config-form-fields">
        <!-- <button id="submit" class="button">Save data</button> -->
        <submit-button>Opslaan</submit-button>
    </div>
</form>  
                
    
</template>
<script>
import SubmitButton from '../ui/SubmitButton.vue'
export default {
  components: { SubmitButton },
    setup() {
        
    },
}
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