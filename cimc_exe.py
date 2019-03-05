# __ author__ Ashish Tyagi
# Report issues or bug ashtyagi@tetrationanaytics.com

import paramiko
import time
import subprocess

#getcimcip():
#open orchestrator connection to get cimc ip's
cmd = "curl -s http://orchestrator.service.consul:8888/api/v1.0/cablecheck |jq . |grep -i cimc| grep -Eo '([0-9]*\.){3}[0-9]*'"
f = open(r'/tmp/cimc.txt','w')
returned_value = subprocess.call(cmd, shell=True, stdout=f)  # returns the exit code in unix
f.close()
print(f)

#Create list of cimc
with open('/tmp/cimc.txt') as cimc:
  content = cimc.readlines()

content = [x.strip() for x in content]
print("Here is the list of CIMC :", content)

#get into cimc and execute the commands.

def logintocimc(ip):
    # VARIABLES THAT NEED CHANGED
    ip = ip
    username = <user>
    password = <password>

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # initiate SSH connection
    remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    print "SSH connection established to %s" % ip

    # Use invoke_shell to establish an 'interactive session'
    remote_conn = remote_conn_pre.invoke_shell()
    print "Interactive SSH session established"

    # Strip the initial router prompt
    output = remote_conn.recv(1000)

    # See what we have
    print output

    # Now let's try to send the cimc command
    remote_conn.send("\n")
    remote_conn.send("scope cimc\n")
    remote_conn.send("show detail\n")

    # Wait for the command to complete
    time.sleep(2)

    output = remote_conn.recv(5000)
    print output

if __name__ == '__main__':
  for cimc_ip in content:
     logintocimc(cimc_ip)
============================================================================
