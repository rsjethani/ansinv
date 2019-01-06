|pic1| |pic2| |pic3| |pic4|

####################################
A Simple Ansible Inventory Generator
####################################

Overview
********
This simple library makes it easier to write *glue* code between infrastructure bringup/deployment and software provisioning stages of a one-click deployment.

Head over to the `wiki page <https://github.com/rsjethani/ansinv/wiki#welcome-to-the-ansinv-wiki>`_ for more expanation about this project.

Installation
************
Simply say::

   pip install ansinv

Usage
*****

Working with ansible inventory hosts
====================================

Creating a host object with optional `host variables <https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#host-variables>`_:
----------------------------------------
::

   host1 = ansinv.AnsibleHost("192.168.10.11", affinity=12, scan="no")

Get a host object's ip/name:
----------------------------
::

   print(host1.name)
   
Read and update a host object's host variables. The ``hostvars`` attribute is essentially a dictionary:
-------------------------------------------------------------------------------------------------------
::

   print(host1.hostvars["scan"])
   host1.hostvars["affinity"] = 5
   host1.hostvars.update(x=100)

Working with ansible inventory groups
=====================================

Creating a group object with optional `group variables <https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#group-variables>`_:
-----------------------------------------
::

   group1 = ansinv.AnsibleGroup("group1", ssh_port=8800)

Read and update a group object's group variables. The ``groupvars`` attribute is essentially a dictionary:
----------------------------------------------------------------------------------------------------------
::

   print(group1.groupvars["ssh_port"])
   group1.groupvars["ssh_port"] = 22
   group1.groupvars.update(x=100)

Adding hosts to a group:
------------------------
::

   group1.add_hosts(host1, host2, ...) # host1, host2, etc. must already exist
   group1.add_hosts(ansinv.AnsibleHost("192.168.12.12", hostvar1="value")) # creating and adding hosts at the same time
   
**Please note:** Adding a host object actually creates a **copy** of the host object under the group object. So to make modifications to a host object after it has been added, use ``AnsibleGroup.host(hostname)`` method.

Get access to a host object using ``AnsibleGroup.host(hostname)`` method:
-------------------------------------------------------------------------
::

   group1.host("192.168.1.12").hostvars["hostvar1"] = "new value"
   
Get a list of all host objects in a group:
------------------------------------------
::

   group1.hosts

Establish parent-child relation between groups:
-----------------------------------------------
::

   child1 = AnsibleGroup("master")
   child2 = AnsibleGroup("worker")
   parent = AnsibleGroup("cluster")
   parent.add_children(child1, child2)
   parent.add_children(parent)   # ValueError when trying to add itself as a child
   child1.add_children(parent)   # ValueError when trying to add a parent group as a child

Check whether the group is the parent of a given group:
-------------------------------------------------------
::

   group1.is_parent_of(group2)   # Returns a bool value

Check whether the group is the child of a given group:
------------------------------------------------------
::

   group1.is_child_of(group2)   # Returns a bool value

Get a list of names (not objects) of all child groups:
------------------------------------------------------
::

   group1.children   # ["child1", "child2", ...]



For more explanation and a full example please refer the `wiki page <https://github.com/rsjethani/ansinv/wiki#welcome-to-the-ansinv-wiki>`_.


.. |pic1| image:: https://img.shields.io/badge/License-MIT-yellow.svg
            :target: https://opensource.org/licenses/MIT

.. |pic2| image:: https://badge.fury.io/py/ansinv.svg
            :target: https://pypi.org/project/ansinv

.. |pic3| image:: https://travis-ci.com/rsjethani/ansinv.svg?branch=master
            :target: https://travis-ci.com/rsjethani/ansinv

.. |pic4| image:: https://codecov.io/gh/rsjethani/ansinv/branch/master/graph/badge.svg
            :target: https://codecov.io/gh/rsjethani/ansinv
