.. _jwnmulder.zyxel_vmg8825.zyxel_vmg8825_facts_module:


*******************************************
jwnmulder.zyxel_vmg8825.zyxel_vmg8825_facts
*******************************************

**Get facts about zyxel_vmg8825 devices.**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Collects facts from network devices running the zyxel_vmg8825 operating system. This module places the facts gathered in the fact tree keyed by the respective resource name.  The facts module will always collect a base set of facts from the device and can enable or disable collection of additional facts.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>gather_network_resources</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.9</div>
                </td>
                <td>
                </td>
                <td>
                        <div>When supplied, this argument will restrict the facts collected to a given subset. Possible values for this argument include all and the resources like interfaces, vlans etc. Can specify a list of values to include a larger subset. Values can also be used with an initial <code><span class='module'>!</span></code> to specify that a specific subset should not be collected.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>gather_subset</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                    <div style="font-style: italic; font-size: small; color: darkgreen">added in 2.2</div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"all"</div>
                </td>
                <td>
                        <div>When supplied, this argument will restrict the facts collected to a given subset. Possible values for this argument include all, min, hardware, config, legacy, and interfaces. Can specify a list of values to include a larger subset. Values can also be used with an initial <code><span class='module'>!</span></code> to specify that a specific subset should not be collected.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    # Gather all facts
    - zyxel_vmg8825_facts:
        gather_subset: all
        gather_network_resources: all

    # Collect only the static_dhcp_table facts
    - zyxel_vmg8825_facts:
        gather_subset:
          - "!all"
          - "!min"
        gather_network_resources:
          - static_dhcp_table

    # Do not collect static_dhcp_table facts
    - zyxel_vmg8825_facts:
        gather_network_resources:
          - "!static_dhcp_table"

    # Collect static_dhcp_table and minimal default facts
    - zyxel_vmg8825_facts:
        gather_subset: min
        gather_network_resources: static_dhcp_table




Status
------


Authors
~~~~~~~

- Jan-Willem Mulder (@jwnmulder)
