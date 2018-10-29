[v1.3.1] 2018-10-30
===================

Changed
-------

* Improved package distribution configuration to be more informative and standardized.
* Small changes to make code Python 2.7.x compatible.



[v1.3.0] 2018-10-29
===================

Added
-----

* Added new public api method **as_ini()** to AnsibleInventory class. This method allows user to get inventory data in Ansible's INI format.



[v1.2.0] 2018-10-28
===================

Added
-----

* **update_ungrouped_hosts** method to public API. This method allows user to add exisitng hosts (which may be part of other groups) to exist as 'ungrouped' also.
