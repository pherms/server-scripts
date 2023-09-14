import subprocess
import os

def monitor_deamons():
#    print("starting monitor")

   ps = subprocess.Popen(('ps', '-ef'), stdout=subprocess.PIPE)
   grep = subprocess.Popen(('grep', '-v', 'grep'), stdin=ps.stdout, stdout=subprocess.PIPE)

   ps.stdout.close()  # Allow ps to receive a SIGPIPE if grep exits.

   grep_daemon = subprocess.Popen(('grep', 'sshd'), stdin=grep.stdout)

   grep.stdout.close() # Allow grep to receive a SIGPIPE if grep_daemon exits

   output = grep_daemon.communicate()[0]

   print(output)

def check_daemon():
   # grep = subprocess.Popen(('systemctl', 'list-units'), stdout=subprocess.PIPE)
   # service = subprocess.Popen(('grep', 'ssh'), stdin=grep.stdout,stdout=subprocess.PIPE)
   # servicename = subprocess.Popen(('awk', '{print $1, $2}'),stdin=service.stdout).communicate()
   # cmd = ['systemctl', 'list-units', '|', 'grep', 'ssh', '|', 'awk', '\'\{print $1, $2\}\'']
   servicename = subprocess.check_output("systemctl status cpupower", shell=True).decode()
   # serviceState = subprocess.check_output("systemctl show -p LoadState --value bla", shell=True).decode()
   servicestate = servicename.find("loades")
   print("Service: {}".format(servicename))
   print("Service: {}".format(servicestate))
   # print("Stae: {}".format(state))
   # systemctl list-units | grep ssh | awk '{print $1, $2}'
   # awk '{print $1, $2}'
   # systemctl show -p Id --value cpupower  --> return service name
   # systemctl show -p LoadState --value cpupower  --> return service name

check_daemon()

   #  ps = subprocess.Popen(('ps', '-ef'), stdout=subprocess.PIPE)
   #  grep = subprocess.Popen(('grep', '-v', 'grep'), stdin=ps.stdout, stdout=subprocess.PIPE)

   #  ps.stdout.close()  # Allow ps to receive a SIGPIPE if grep exits.

   #  grep_daemon = subprocess.Popen(('grep', 'sshd'), stdin=grep.stdout)

   #  grep.stdout.close() # Allow grep to receive a SIGPIPE if grep_daemon exits

   #  output = grep_daemon.communicate()[0]