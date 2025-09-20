===========================
Zyxel VMG8825 Release Notes
===========================

.. contents:: Topics

v0.4.1
======

Minor Changes
-------------

- Github workflow and linting fixes for ansible-core 2.20

v0.4.0
======

Minor Changes
-------------

- Added new encryption and CSRF features to support latest TMNL firmware requirements which became required since V5.50(ABPY.1)b21_20230112

v0.3.0
======

Release Summary
---------------

Added zyxel_vmg8825_firewall and zyxel_vmg8825_firewall_acls modules and some minor bugfixes

Minor Changes
-------------

- Added new firewall module
- Added new firewall_acls module

Bugfixes
--------

- nat_port_forwards - fixed TCP/UDP protocol option. The option 'TCP_UDP' was invalid and is now corrected to 'ALL'

New Modules
-----------

- zyxel_vmg8825_firewall - Manages firewall config of zyxel_vmg8825
- zyxel_vmg8825_firewall_acls - Manages firewall ACL entries of zyxel_vmg8825

v0.2.0
======

Release Summary
---------------

Added zyxel_vmg8825_nat_port_forwards module

New Modules
-----------

- zyxel_vmg8825_nat_port_forwards - Manages nat port forward entries of zyxel_vmg8825

v0.1.0
======

Release Summary
---------------

Initial release containing the zyxel_vmg8825_static_dhcp module

New Plugins
-----------

Httpapi
~~~~~~~

- zyxel_vmg8825 - HttpApi Plugin for Zyxel VMG 8825

New Modules
-----------

- zyxel_vmg8825_dal_rpc - Zyxel Module for interacting with the Zyxel DAL API
- zyxel_vmg8825_facts - Get facts about zyxel_vmg8825 devices.
- zyxel_vmg8825_static_dhcp - Manages static_dhcp entries of zyxel_vmg8825
