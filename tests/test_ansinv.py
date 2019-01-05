import json
import re


import pytest


from ansinv import *


class TestAnsibleHost:
    def test_host_without_hostvars(self):
        test_host = AnsibleHost("host1")
        assert str(test_host) == "host1"

    def test_host_with_hostvars(self):
        test_host = AnsibleHost("host1", var1="val1", var2="val2")
        assert str(test_host) == "host1 var1=val1 var2=val2"


class TestAnsibleGroup:
    def test_empty_group(self):
        test_grp1 = AnsibleGroup("grp1")
        assert str(test_grp1) == ""

    def test_group_with_groupvars_hosts_and_children(self):
        test_grp1 = AnsibleGroup("grp1", var1="val1", var2="val2")
        test_grp1.add_hosts(AnsibleHost("h1"), AnsibleHost("h2"))
        test_grp1.add_children(AnsibleGroup("child1"), AnsibleGroup("child2"))
        assert str(test_grp1) == "\n[grp1]\nh1\nh2\n\n[grp1:vars]\nvar1=val1\nvar2=val2\n\n[grp1:children]\nchild1\nchild2"

    def test_group_and_hosts_relation(self):
        test_grp1 = AnsibleGroup("grp1")
        test_grp1.add_hosts(AnsibleHost("h1"), AnsibleHost("h2"))

        assert len(test_grp1.hosts) == 2
        assert test_grp1.host("dummy") == None
        assert test_grp1.host("h1").name == "h1"

    def test_group_and_children_relation(self):
        test_grp1 = AnsibleGroup("grp1")
        test_grp1.add_children(AnsibleGroup("child1"), AnsibleGroup("child2"))

        assert len(test_grp1.children) == 2
        assert test_grp1.child("dummy") == None
        assert test_grp1.child("child1") == "child1"


class TestAnsibleInventory:
    def test_empty_inventory(self):
        test_inv = AnsibleInventory()
        assert str(test_inv) == ""

    def test_full_inventory(self):
        test_inv = AnsibleInventory(AnsibleHost("ugh1"), AnsibleHost("ugh2"))

        g1 = AnsibleGroup("g1")
        g1.add_hosts(AnsibleHost("h1"), AnsibleHost("h2", h2var1="h2val1", h2var2="h2val2"))

        g2 = AnsibleGroup("g2", g2var1="g2val1")
        g2.add_hosts(AnsibleHost("h3"))

        g3 = AnsibleGroup("g3")
        g3.add_children(g1,g2)

        test_inv.add_groups(g1, g2, g3)

        assert str(test_inv) == "ugh1\nugh2\n\n[g1]\nh1\nh2 h2var1=h2val1 h2var2=h2val2\n\n[g2]\nh3\n\n[g2:vars]\ng2var1=g2val1\n\n[g3:children]\ng1\ng2"

