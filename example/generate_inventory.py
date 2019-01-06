#!/usr/bin/env python3

# PS: No exception/error handling present in order to keep things simple

import json
from ansinv import *


# Initialize empty inventory
inventory = AnsibleInventory()

# Create required groups
for grp_name in "master", "worker", "monitoring", "k8s-cluster":
    inventory.add_groups(AnsibleGroup(grp_name))

# Establish parent-child relation if any between groups
inventory.group("k8s-cluster").add_children(inventory.group("master"), inventory.group("worker"))

# Add groupvars if any to groups
inventory.group("monitoring").groupvars.update(elastic_port=6000, logstash_port=6100, kibana_port=3000)
inventory.group("all").groupvars.update(ansible_user="testuser", ansible_ssh_private_key_file="cloud.key")

# load terraform state file
with open("terraform.tfstate") as file:
    state = json.load(file)

# Add hosts to groups and/or inventory
for resource, res_info in state["modules"][0]["resources"].items():
    if res_info["type"] == "libvirt_domain":
        host_ip = res_info["primary"]["attributes"]['network_interface.0.addresses.0']
        name = res_info["primary"]["attributes"]['name']

        # "libvirt_domain.worker.0" -> "libvirt_domain", "worker", ("0",)
        grp_name = resource.split(".")[1]

        # add host to repective group
        inventory.group(grp_name).add_hosts(AnsibleHost(host_ip, host_name=name))

# Write inventory data to a file in ini format.
with open("inventory", "w") as file:
    file.write(str(inventory))
