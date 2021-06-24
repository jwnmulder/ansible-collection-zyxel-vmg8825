.. _jwnmulder.zyxel_vmg8825.zyxel_ping_module:


**********************************
jwnmulder.zyxel_vmg8825.zyxel_ping
**********************************

**Zyxel Module**



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Zyxel module



Requirements
------------
The below requirements are needed on the host that executes this module.

- zyxelclient_vmg8825





Examples
--------

.. code-block:: yaml

    - name: Get AVI API version
        community.network.avi_api_version:
          controller: ""
          username: ""
          password: ""
          tenant: ""
        register: avi_controller_version



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>obj</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>success, changed</td>
                <td>
                            <div>Avi REST resource</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Jan-Willem Mulder (@jwnmulder)
