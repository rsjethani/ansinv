|pic1| |pic2| |pic3| |pic4|


####################################
A Simple Ansible Inventory Generator
####################################


=Overview=
**********
This simple library makes it easier to write the **glue code** between infrastructure bringup/orchestration and software provisioning stages of a one-click deployment.

Head over to the `wiki page <https://github.com/rsjethani/ansinv/wiki#welcome-to-the-ansinv-wiki>`_ for more explanation about this project.


=Installation=
**************
::

   pip install ansinv


=Working with inventory hosts=
******************************

Creating a host with optional `host variables <https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#host-variables>`_:
---------------------------------------------------------------------------------------------------------------------------------------------------
::

   host1 = ansinv.AnsibleHost("192.168.10.11", affinity=12, scan="no")

Get a host's ip/name using ``AnsibleHost.name`` attribute:
----------------------------------------------------------
::

   print(host1.name)
   
Read/Update a host's host variables using ``AnsibleHost.hostvars`` attribute:
-----------------------------------------------------------------------------
::

   print(host1.hostvars["scan"])
   host1.hostvars["affinity"] = 5
   host1.hostvars.update(x=100)


=Working with inventory groups=
*******************************

Creating a group with optional `group variables <https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#group-variables>`_:
---------------------------------------------------------------------------------------------------------------------------------------------------
::

   group1 = ansinv.AnsibleGroup("group1", ssh_port=8800)

Get a group's name using ``AnsibleGroup.name`` attribute:
----------------------------------------------------------
::

   print(group1.name)

Read/Update a group's group variables using the ``AnsibleGroup.groupvars`` attribute:
-------------------------------------------------------------------------------------
::

   print(group1.groupvars["ssh_port"])
   group1.groupvars["ssh_port"] = 22
   group1.groupvars.update(x=100)

Adding hosts to a group using ``AnsibleGroup.add_hosts`` method:
----------------------------------------------------------------
::

   group1.add_hosts(host1, host2, ...) # host1, host2, etc. must already exist
   group1.add_hosts(ansinv.AnsibleHost("192.168.12.12", hostvar1="value")) # creating and adding hosts at the same time
  
**Please note:** Adding a host actually creates a **copy** of the host object under the group. So to make modifications to a host object after it has been added, use ``AnsibleGroup.host`` method as described below.

Get access to a member host using ``AnsibleGroup.host('hostname')`` method:
---------------------------------------------------------------------------
::

   group1.host("192.168.1.12").hostvars["hostvar1"] = "new value"

**Please note:** The host() method will always return the first occurrence of the given 'hostname', even if there are multiple hosts with same name in the group. This behavior assumes that even though you are allowed to have multiple hosts with same name but you will never actually require such a case.
   
Get a list of all host objects in a group using ``AnsibleGroup.hosts`` attribute:
---------------------------------------------------------------------------------
::

   print(group1.hosts[0].name)

Establish parent-child relation between groups using ``AnsibleGroup.add_children`` method:
------------------------------------------------------------------------------------------
::

   child1 = AnsibleGroup("master")
   child2 = AnsibleGroup("worker")
   parent = AnsibleGroup("cluster")
   parent.add_children(child1, child2)
   parent.add_children(parent)   # ValueError when trying to add itself as a child
   child1.add_children(parent)   # ValueError when trying to add a parent group as a child

Check whether the group is a parent of given group using ``AnsibleGroup.is_parent_of`` method:
----------------------------------------------------------------------------------------------
::

   group1.is_parent_of(group2)   # Returns a bool value

Check whether the group is a child of given group using ``AnsibleGroup.is_child_of`` method:
--------------------------------------------------------------------------------------------
::

   group1.is_child_of(group2)   # Returns a bool value

Get a list of all child objects using ``AnsibleGroup.children`` attribute:
----------------------------------------------------------------------------------
::

   print(group1.children[0].name)


=Working with the inventory itself=
***********************************

Creating an inventory:
----------------------
::

   inv = AnsibleInventory()   # empty inventory
   inv = AnsibleInventory(AnsibleHost("h1"), AnsibleHost("h2"))   # inventory initialized with two ungrouped hosts

Add (ungrouped) hosts to the inventory using ``AnsibleInventory.add_hosts`` method:
-----------------------------------------------------------------------------------
::

   h1 = AnsibleHost("h1")
   h2 = AnsibleHost("h2")
   inv.add_hosts(h1, h2)

**Please note:** The hosts added directly to the inventory are 'ungrouped' hosts i.e. they will not appear under other groups.

Add groups to the inventory using ``AnsibleInventory.add_groups`` method:
-------------------------------------------------------------------------
::

   g1 = AnsibleGroup("g1")
   g2 = AnsibleGroup("g2")
   inv.add_groups(g1, g2)

**Please note:** Adding a host/group actually creates a **copy** of the host/group object under the inventory. So to make modifications to a host/group object after it has been added, use ``AnsibleInventory.host(hostname)``/``AnsibleInventory.group(groupname)`` methods as described below.

Get an *ungrouped* host object from the inventory using ``AnsibleInventory.host`` method:
-----------------------------------------------------------------------------------------
::

   print(inv.host("h1"))
   inv.host("h1").hostvars["somevar"] = 111  # modify an ungrouped host after it has been added to the inventory

Get a group object from the inventory using ``AnsibleInventory.group('groupname')`` method:
-------------------------------------------------------------------------------------------
::

   inv.group("g1").groupvars["x"] = 1111
   inv.group("g1").host("h1").hostvars["somevar"] = 333

**Please note:** The group() method will always return the first occurrence of the given 'groupname', even if there are multiple groups with same name in the inventory. This behavior assumes that even though you are allowed to have multiple groups with same name but you will never actually require such a case.

Get a list of all group objects from the inventory using ``AnsibleInventory.groups`` attribute:
-----------------------------------------------------------------------------------------------
::

   for grp in inv.groups:
      print(grp.name)
      
Get the whole inventory as a string object:
-------------------------------------------
The string version of the inventory is in the INI format which you can simply write to a file and pass the file to Ansible.
::
 
   inv = AnsibleInventory()
   ...   # add some groups and hosts
   print(str(inv))
   with open("inventory", "w") as f:
      f.write(str(inv))

For more explanation and a full example please visit the `wiki page <https://github.com/rsjethani/ansinv/wiki#welcome-to-the-ansinv-wiki>`_.


.. |pic1| image:: https://img.shields.io/badge/License-MIT-yellow.svg
            :target: https://opensource.org/licenses/MIT

.. |pic2| image:: https://badge.fury.io/py/ansinv.svg
            :target: https://pypi.org/project/ansinv

.. |pic3| image:: https://travis-ci.com/rsjethani/ansinv.svg?branch=master
            :target: https://travis-ci.com/rsjethani/ansinv

.. |pic4| image:: https://codecov.io/gh/rsjethani/ansinv/branch/master/graph/badge.svg
            :target: https://codecov.io/gh/rsjethani/ansinv

