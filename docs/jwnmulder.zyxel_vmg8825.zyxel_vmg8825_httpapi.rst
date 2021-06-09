.. _jwnmulder.zyxel_vmg8825.zyxel_vmg8825_httpapi:


*************************************
jwnmulder.zyxel_vmg8825.zyxel_vmg8825
*************************************

**Zyxel Web REST interface**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- plugin that uses the Zyxel Web REST interface to manage the router. Main usecase is to send commands on the /DAL interface




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>eos_use_sessions</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                                <div>env:ANSIBLE_EOS_USE_SESSIONS</div>
                                <div>var: ansible_eos_use_sessions</div>
                    </td>
                <td>
                        <div>Specifies if sessions should be used on remote host or not</div>
                </td>
            </tr>
    </table>
    <br/>








Status
------


Authors
~~~~~~~

- Ansible Networking Team


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
