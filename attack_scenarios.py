import subprocess

# 
# 
# TODO: Define create_file_access_scenario() with sandboxed and unsandboxed processes

# Simulates unauthorized access to a file
#
#
def fileAcessScenario():
    with open("/etc/shadow", "r") as f: # permission denied as of right now
        data = f.read()
        print(data)

# TODO: Define create_network_access_scenario()

def networkAcessScenario():
    subprocess.run(["curl", "http://example.com", "-o", "/tmp/network_test.html"])

# TODO: Define create_privilege_escalation_scenario()

def privelegeEscelationScenario():
    subprocess.run(["sudo", "touch", "/root/hacked.txt"], stderr=subprocess.PIPE)

# TODO: Return list of processes for each scenario

if __name__ == "__main__":
    fileAcessScenario()
