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

    # Test adding existing host but with different hostvars
    test_inventory.add_host("h2", var1="new_value")
    assert (json.loads(str(test_inventory))["_meta"]["hostvars"]["h2"]
        == {"var1": "new_value", "var2": "val2"}
    )


def test_get_hostvars():
    test_inventory = AnsibleInventory()

    with pytest.raises(HostsNotFound) as err:
        test_inventory.get_hostvars("h1")
    assert err.value.args == ("h1",)

    hostvars = {"var1": "val1"}
    test_inventory.add_host("h1", **hostvars)
    assert test_inventory.get_hostvars("h1") == hostvars


def test_get_groupvars():
    test_inventory = AnsibleInventory()

    with pytest.raises(GroupsNotFound) as err:
        test_inventory.get_groupvars("g1")
    assert err.value.args == ("g1",)

    groupvars = {"var1": "val1"}
    test_inventory.add_group("g1", **groupvars)
    assert test_inventory.get_groupvars("g1") == groupvars

