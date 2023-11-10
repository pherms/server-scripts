const button = document.getElementById('button');
button.hidden = true; // kan later weg. Handig voor testen
const submitButton = document.getElementById('submit');

const filetype = document.getElementById('filetype');
const backuppath = document.getElementById('backuppath');
const logfilepath = document.getElementById('logfilepath');
const scriptspath = document.getElementById('scriptspath');
const apiurl = document.getElementById('apiurl');
const sourcesLocation = document.getElementById('sourcesLocation');
const compression = document.getElementById('compression');
const backupserver = document.getElementById('backupserver');
const copycommand = document.getElementById('copycommand');
const remotefilepath = document.getElementById('remotefilepath');
const mailserver = document.getElementById('mailserver');
const mailRecipient = document.getElementById('mailRecipient');
const mailSender = document.getElementById('mailSender');
const debug = document.getElementById('debug');
const hostType = document.getElementById('hostType');
const timerUnits = document.getElementById('timerUnits');
const servicesToInstall = document.getElementById('servicesToInstall');
const servicesToCopy = document.getElementById('servicesToCopy');

function loadData() {
    fetch('http://localhost:8081/')
    .then(response => response.json())
    .then(data => {
        console.log(data.ip);
        console.log(data.port);
        console.log(data.enable);
        
        filetype.value = data.filetype;
        backuppath.value = data.backuppath;
        logfilepath.value = data.logfilepath;
        scriptspath.value = data.scriptspath;
        apiurl.value = data.apiurl;
        sourcesLocation.value = data.sourcesLocation;
        compression.value = data.compression;
        backupserver.value = data.backupserver;
        copycommand.value = data.copycommand;
        remotefilepath.value = data.remotefilepath;
        mailserver.value = data.mailserver;
        mailRecipient.value = data.mailRecipient;
        mailSender.value = data.mailSender;
        debug.value = data.debug;
        hostType.value = data.hostType;
        timerUnits.value = data.timerUnits;
        servicesToInstall.value = data.servicesToInstall;
        servicesToCopy.value = data.servicesToCopy;
        console.log(data);
    });
};

button.addEventListener('click', () => loadData());
// button.addEventListener('click', () => {
//     fetch('http://localhost:8081/')
//         .then(response => response.json())
//         .then(data => {
//             console.log(data.ip);
//             console.log(data.port);
//             console.log(data.enable);
            
//             responseDiv.innerHTML = data;
//             ip.value = data.ip;
//             port.value = data.port;
//             enabled.value = data.enable;
//             console.log(data);
//         });
// });

submitButton.addEventListener('click', () => {
    fetch('http://localhost:8081/update', {
        method: "PUT",
        body: JSON.stringify({filetype:filetype.value, backuppath:backuppath.value, logfilepath:logfilepath.value, scriptspath:scriptspath.value, apiurl:apiurl.value, sourcesLocation:sourcesLocation.value, compression:compression.value, backupserver:backupserver.value , copycommand:copycommand.value, remotefilepath:remotefilepath.value, mailserver:mailserver.value, mailRecipient:mailRecipient.value, mailSender:mailSender.value, debug:debug.value, hostType:hostType.value, timerUnits:timerUnits.value, servicesToInstall:servicesToInstall.value, servicesToCopy:servicesToCopy.value  }),
        headers: { "Content-type": "application/json; charset=UTF-8"}
    })
    .then((response) => response.json())
    .then((json) => console.log(json));
});