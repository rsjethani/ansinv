import json


import pytest


from ansinv import *


@pytest.fixture
def empty_inventory():
    """Represents an empty inventory dict object"""
    return {
        "_meta": {
                "hostvars": {}
        },
        "all": {
            "vars": {},
            "hosts": [],
            "children": ["ungrouped"]
        },
        "ungrouped": {
            "hosts": []
        }
    }


def test_empty_inventory(empty_inventory):
    expected_inventory = empty_inventory
    test_inventory = AnsibleInventory()
    assert json.loads(str(test_inventory)) == expected_inventory


def test_add_host(empty_inventory):
    expected_inventory = empty_inventory
    test_inventory = AnsibleInventory()

    new_hosts = {"h1": {}, "h2": {"var1": "val1", "var2": "val2"}}
    for host, hostvars in new_hosts.items():
        expected_inventory["all"]["hosts"].append(host)
        expected_inventory["ungrouped"]["hosts"].append(host)
        expected_inventory["_meta"]["hostvars"][host] = hostvars

        test_inventory.add_host(host, **hostvars)

        assert host in test_inventory.hosts
        assert host in test_inventory.ungrouped
        assert (json.loads(str(test_inventory))["_meta"]["hostvars"][host]
            == expected_inventory["_meta"]["hostvars"][host]
        )

    assert len(test_inventory.hosts) == len(new_hosts)

    # Test: Adding existing host should be a no-op
    test_inventory.add_host("h1", var1="value")
    assert json.loads(str(test_inventory))["_meta"]["hostvars"]["h1"] == expected_inventory["_meta"]["hostvars"]["h1"]


def test_get_hostvars():
    test_inventory = AnsibleInventory()

    with pytest.raises(HostsNotFound):
        test_inventory.get_hostvars("h1")

    hostvars = {"var1": "val1"}
    test_inventory.add_host("h1", **hostvars)
    assert test_inventory.get_hostvars("h1") == hostvars


def test_update_hostvars():
    test_inventory = AnsibleInventory()
    hostvars = {"var1": "val1"}

    with pytest.raises(HostsNotFound):
        test_inventory.update_hostvars("h1", **hostvars)

    test_inventory.add_host("h1")
    test_inventory.update_hostvars("h1", **hostvars)
    assert test_inventory.get_hostvars("h1") == hostvars


def test_add_group(empty_inventory):
    expected_inventory = empty_inventory
    test_inventory = AnsibleInventory()

    new_groups = {"g1": {}, "g2": {"var1": "val1", "var2": "val2"}}
    for group, groupvars in new_groups.items():
        expected_inventory[group] = {
            "vars": groupvars,
            "hosts": [],
            "children": []
        }
        expected_inventory["all"]["children"].append(group)

        test_inventory.add_group(group, **groupvars)

        assert json.loads(str(test_inventory))[group] == expected_inventory[group]
        assert group in json.loads(str(test_inventory))["all"]["children"]

    # '1' is for the implied "all" group
    assert len(test_inventory.groups) == len(new_groups) + 1

    # Test: Adding existing group should be a no-op
    test_inventory.add_group("g1", var1="value")
    assert json.loads(str(test_inventory))["g1"] == expected_inventory["g1"]

    # Test use of reserved names for a new group
    with pytest.raises(ValueError):
        test_inventory.add_group("_meta")


def test_get_groupvars():
    test_inventory = AnsibleInventory()

    with pytest.raises(GroupsNotFound):
        test_inventory.get_groupvars("g1")

    groupvars = {"var1": "val1"}
    test_inventory.add_group("g1", **groupvars)
    assert test_inventory.get_groupvars("g1") == groupvars


def test_update_groupvars():
    test_inventory = AnsibleInventory()
    groupvars = {"var1": "val1"}

    with pytest.raises(GroupsNotFound):
        test_inventory.update_groupvars("g1", **groupvars)

    test_inventory.add_group("g1")
    test_inventory.update_groupvars("g1", **groupvars)
    assert test_inventory.get_groupvars("g1") == groupvars


def test_add_hosts_to_group():
    test_inventory = AnsibleInventory("h1", "h2", "h3")
    test_inventory.add_group("g1")

    with pytest.raises(GroupsNotFound):
        test_inventory.add_hosts_to_group("foo", "h1")

    with pytest.raises(HostsNotFound):
        test_inventory.add_hosts_to_group("g1", "foo")
    
    test_inventory.add_hosts_to_group("g1", "h1", "h2")
    assert "h1", "h2" in json.loads(str(test_inventory))["g1"]["hosts"]
    assert len(json.loads(str(test_inventory))["g1"]["hosts"]) == 2


def test_add_children_to_group():
    test_inventory = AnsibleInventory()
    test_inventory.add_group("g1")
    test_inventory.add_group("g2")
    test_inventory.add_group("g3")

    with pytest.raises(GroupsNotFound):
        test_inventory.add_children_to_group("g1", "g2", "g3", "foo")

    with pytest.raises(ValueError):
        test_inventory.add_children_to_group("g1", "g1")

    test_inventory.add_children_to_group("g1", "g2", "g3")
    assert "g2", "g3" in json.loads(str(test_inventory))["g1"]["children"]
    assert len(json.loads(str(test_inventory))["g1"]["children"]) == 2


def test_keep_hosts_ungrouped_also():
    test_inventory = AnsibleInventory("h1", "h2")
    test_inventory.add_group("g1")
    test_inventory.add_hosts_to_group("g1", "h1")
    test_inventory.keep_hosts_ungrouped_also("h1")
    assert "h1", "h2" in test_inventory.ungrouped


def test_groups_property():
    test_inventory = AnsibleInventory()
    test_inventory.add_group("g1")
    test_inventory.add_group("g2")
    test_inventory.add_group("g3")

    assert "_meta", "ungrouped" not in test_inventory.groups
    assert len(test_inventory.groups) == 3 + 1

