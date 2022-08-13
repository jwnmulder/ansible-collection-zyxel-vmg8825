# Zyxel VMG8825 Ansible Collection

[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-ready--to--code-908a85?logo=gitpod)](https://gitpod.io/#https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825)
[![GitHub Actions pre-commit status](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/workflows/pre-commit/badge.svg?branch=main)](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/actions/workflows/pre-commit.yml?query=branch%3Amain)
[![GitHub Actions ansible-test status](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/workflows/ansible-test/badge.svg?branch=main)](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/actions/workflows/ansible-test.yml?query=branch%3Amain)

The Ansible Zyxel collection includes a variety of Ansible content to help automate the management of Zyxel VMG8825 routers.

This collection has been tested against Zyxel VMG8825-T50.

For now only the `zyxel_vmg8825_nat_port_forwards` and `zyxel_vmg8825_static_dhcp` modules have been tested. Other modules are work in progress

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

For collections that support Ansible 2.9, please ensure you update your `network_os` to use the
fully qualified collection name (for example, `cisco.ios.ios`).
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
[jwnmulder.zyxel_vmg8825.zyxel_vmg8825_firewall](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_vmg8825_firewall_module.rst)|Manages firewall config of zyxel_vmg8825
[jwnmulder.zyxel_vmg8825.zyxel_vmg8825_firewall_acls](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_vmg8825_firewall_acls_module.rst)|Manages firewall ACL entries of zyxel_vmg8825
[jwnmulder.zyxel_vmg8825.zyxel_vmg8825_nat_port_forwards](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_vmg8825_nat_port_forwards_module.rst)|Manages nat port forward entries of zyxel_vmg8825
[jwnmulder.zyxel_vmg8825.zyxel_vmg8825_ping](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_vmg8825_ping_module.rst)|Zyxel Module for sending PINGTEST
[jwnmulder.zyxel_vmg8825.zyxel_vmg8825_static_dhcp](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_vmg8825_static_dhcp_module.rst)|Manages static_dhcp entries of zyxel_vmg8825

<!--end collection content-->

## Installing this collection

You can install the Zyxel collection with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install jwnmulder.zyxel_vmg8825
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - jwnmulder.zyxel_vmg8825
```

## Using this collection

This collection includes [network resource modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html).

### Using modules from the Zyxel collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `jwnmulder.zyxel_vmg8825.zyxel_vmg8825_static_dhcp`.
The following example task replaces configuration changes in the existing configuration on a Zyxel router, using the FQCN:

```yaml
---
  - name: Configure static_dhcp
    jwnmulder.zyxel_vmg8825.zyxel_vmg8825_static_dhcp:
      config:
        - br_wan: Default
          enable: True
          mac_addr: "01:01:01:01:01:02"
          ip_addr: "192.168.0.2"
      state: merged
```

## Contributing to this collection

If you want to clone this repository (or a fork of it) to improve it, you can proceed as follows:

1. Strongly recommended, ensure `pre-commit` and `direnv` are installed
2. Create a directory `ansible_collections/jwnmulder`
3. In there, checkout this repository (or a fork) as `zyxel_vmg8825`
4. In the zyxel_vmg8825 dir, run the following commands to setup a python venv

    ```bash
    scripts/ensure-venv.sh
    . .venv/bin/activate
    ```

5. In the zyxel_vmg8825 dir, run the following command 'ansible-galaxy collection install ansible.netcommon'
6. Setup pre-commit by running `pre-commit install` in the zyxel_vmg8825 dir
7. To ensure vscode can run pytest, add the following to your .env file

    ```text
    PYTHONPATH=../../../
    ```

### ansible-test

Using ansible-test

1. Copy inventory.networking.template to inventory.networking and modify accordingly. You also need a Zyxel router. This is needed for the network-integration tests
2. To run all tests: `./scripts/run-all-tests.sh`

### ansible-test debugging tips

```bash
# --debug will trigger logging to /tmp/q
ansible-test network-integration -v --debug
```

### Generate / update resource module configurations

```bash
# https://github.com/ansible-network/cli_rm_builder
ansible-galaxy collection install git+https://github.com/ansible-network/cli_rm_builder.git

cd rm_builder
ansible-playbook -e rm_dest=$(pwd)/.. generate_all.yml
ansible-playbook -e rm_dest=$(pwd)/.. update_all.yml
```

## Wish list

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
