import subprocess

def monitor_deamons():
   print("starting monitor")

   ps = subprocess.Popen(('ps', '-ef'), stdout=subprocess.PIPE)
   grep = subprocess.Popen(('grep', '-v', 'grep'), stdin=ps.stdout, stdout=subprocess.PIPE)

   ps.stdout.close()  # Allow ps to receive a SIGPIPE if grep exits.

   grep_daemon = subprocess.Popen(('grep', 'sshda'), stdin=grep.stdout)

   grep.stdout.close() # Allow grep to receive a SIGPIPE if grep_daemon exits

   output = grep_daemon.communicate()[0]

   print(output)

monitor_deamons()