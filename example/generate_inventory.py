#!/usr/bin/env python3

# PS: No exception/error handling present in order to keep things simple

import json


import ansinv


# Initialize empty inventory
inventory = ansinv.AnsibleInventory()

# Create required groups
for group in "manager", "worker", "monitoring", "cluster":
    inventory.add_group(group)

# Establish parent-child relation if any between groups
inventory.add_children_to_group("cluster", "manager", "worker", "monitoring")

# Add groupvars if any to groups
inventory.update_groupvars("monitoring", elastic_port=6000, logstash_port=6100, kibana_port=3000)
inventory.update_groupvars("all", ansible_user="testuser", ansible_ssh_private_key_file="cloud.key")

# load terraform state file
with open("terraform.tfstate.example") as file:
    state = json.load(file)

# Add hosts to inventory
for resource, res_info in state["modules"][0]["resources"].items():
    if res_info["type"] == "libvirt_domain":
        host_ip = res_info["primary"]["attributes"]['network_interface.0.addresses.0']

        # "libvirt_domain.worker.0" -> "libvirt_domain", "worker", ("0",)
        _, group, *num = resource.split(".")
        num = num[0] if len(num) != 0 else "0"

        # add host to repective group
        inventory.add_host(host_ip, host_name="{}-{}".format(group, num))
        inventory.add_hosts_to_group(group, host_ip)

# Write inventory data to a file in ini format.
with open("inventory.example", "w") as file:
    file.write(inventory.as_ini())
