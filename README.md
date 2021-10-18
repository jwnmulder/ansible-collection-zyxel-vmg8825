# Zyxel VMG8825 Ansible Collection

[![GitHub Actions pre-commit status](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/workflows/pre-commit/badge.svg?branch=main)](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/actions/workflows/pre-commit.yml?query=branch%3Amain)
[![GitHub Actions ansible-test status](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/workflows/ansible-test/badge.svg?branch=main)](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/actions/workflows/ansible-test.yml?query=branch%3Amain)
[![GitHub Actions ci status](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/workflows/ci/badge.svg?branch=main)](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/actions/workflows/ci.yml?query=branch%3Amain)

## Usage instructions

TODO

Collection tested on Zyxel VMG8825-T50

For now only the zyxel_vmg8825_static_dhcp module has been tested. Others modules are work in progres

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## Included content
<!--start collection content-->
### Httpapi plugins
Name | Description
--- | ---
[jwnmulder.zyxel_vmg8825.zyxel_vmg8825](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_vmg8825_httpapi.rst)|HttpApi Plugin for Zyxel VMG 8825

### Modules
Name | Description
--- | ---
[jwnmulder.zyxel_vmg8825.zyxel_vmg8825_dal_rpc](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_vmg8825_dal_rpc_module.rst)|Zyxel Module for interacting with the Zyxel DAL API
[jwnmulder.zyxel_vmg8825.zyxel_vmg8825_facts](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_vmg8825_facts_module.rst)|Get facts about zyxel_vmg8825 devices.
[jwnmulder.zyxel_vmg8825.zyxel_vmg8825_ping](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_vmg8825_ping_module.rst)|Zyxel Module for sending PINGTEST
[jwnmulder.zyxel_vmg8825.zyxel_vmg8825_static_dhcp](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_vmg8825_static_dhcp_module.rst)|Manages static_dhcp entries of zyxel_vmg8825

<!--end collection content-->

## Contributing to this collection

We're following the general Ansible contributor guidelines; see [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html).

If you want to clone this repositority (or a fork of it) to improve it, you can proceed as follows:

1. Strongly recommended, ensure `pre-commit` and `direnv` are installed
2. Create a directory `ansible_collections/jwnmulder`
3. In there, checkout this repository (or a fork) as `zyxel_vmg8825`
4. In the zyxel_vmg8825 dir, run the following commands to setup a python venv

        ```bash
        bin/ensure-venv.sh
        . .venv/bin/activate
        ```
5. In the zyxel_vmg8825 dir, run the following command 'ansible-galaxy collection install ansible.netcommon'
6. Setup pre-commit by runnning `pre-commit install` in the zyxel_vmg8825 dir

### ansible-test

Using ansible-test

1. Copy inventory.networking.template to inventory.networking and modify accordingly
2. To run all tests: `./run-all-tests`

### ansible-test debugging tips

```bash
# --debug will trigger logging to /tmp/q
ansible-test network-integration -v --debug
```

### generate / update resource module configurations

```bash
# https://github.com/ansible-network/cli_rm_builder
ansible-galaxy collection install git+https://github.com/ansible-network/cli_rm_builder.git

ansible-playbook -e rm_dest=$(pwd) rm_builder/generate_all.yml
ansible-playbook -e rm_dest=$(pwd) rm_builder/update_all.yml
```

## Whish list

### status

<https://192.168.0.1/cgi-bin/DAL?oid=status>

Lots of info useful for facts

```json
{
    "result": "ZCFG_SUCCESS",
    "ReplyMsg": "X_ZYXEL_ConnectionType",
    "ReplyMsgMultiLang": "",
    "Object": [
        {
            "DeviceInfo": {
            },
            "SystemInfo": {
            },
            "FirewallInfo": {
            },
            "LanPortInfo": [
            ]
        }
    ]
}
```

### nat (port forwarding)

<https://192.168.0.1/cgi-bin/DAL?oid=nat>

Interface can be any of VD_Internet, ETH_Ethernet or ADSL_Ethernet
ETH_Internet=IP.Interface.7 (lookup via <https://192.168.0.1/cgi-bin/WAN_LAN_LIST_Get>)

Idea: WAN_LAN_LIST could be part of facts?

```json
{"result":"ZCFG_SUCCESS","ReplyMsg":"InternalClient","ReplyMsgMultiLang":"","Object":[{"Enable":true,"Protocol":"TCP","Description":"app forward","Interface":"IP.Interface.7","ExternalPortStart":443,"ExternalPortEnd":443,"InternalPortStart":1443,"InternalPortEnd":1443,"InternalClient":"192.168.0.201","SetOriginatingIP":false,"OriginatingIpAddress":"","Index":1,"X_ZYXEL_AutoDetectWanStatus":false}]}
```
