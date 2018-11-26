[v1.3.3] 2018-11-26
===================

Added
-----
* Detailed documentation.
* Example code for the user.


[v1.3.2] 2018-11-26
===================

Added
-----
* Travis CI integration
* pytest based unit tests
* 'codecov' based code coverage reporting
* Badges for license, latest pypi release, build status, code coverage.

Changed
-------
* 'add_host' will no longer update hostvars when the 'host' already exists. Updation of hostvars will only be done by 'update_hostvars' function. Same goes for 'add_group' and 'update_groupvars'.


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

