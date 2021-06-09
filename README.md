# Zyxel VMG8825 Ansible Collection

[![GitHub Actions pre-commit status](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/workflows/pre-commit/badge.svg?branch=main)](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/actions/workflows/pre-commit.yml?query=branch%3Amain)
[![GitHub Actions ci status](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/workflows/ci/badge.svg?branch=main)](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/actions/workflows/ci.yml?query=branch%3Amain)

## ansible-test

```bash
pip install wheel

cd collections && ansible-galaxy collection install ansible.netcommon -p .
ansible-test sanity -v --color --docker --python 3.8
```

## Ansible network resource module: zyxel_static_dhcp

This README was auto generated but should be modified.  It should contain information and examples
for the collection that was generated if the collection is distributed independently.

## library

## zyxel

<https://github.com/ThomasRinsma/vmg8825scripts>

```bash
pip3 install pycryptodome
```

## other stuff

# docs

* api_context from https://docs.ansible.com/ansible/latest/collections/community/network/avi_httppolicyset_module.html
https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html

https://github.com/fortinet-ansible-dev/ansible-galaxy-fortios-collection/blob/fos_v6.0.0/galaxy_2.0.1/plugins/httpapi/fortios.py
https://openwrt.org/inbox/toh/zyxel/zyxel_vmg8825-t50

zyxel
pyzyxel
zyxel-api
zyxel-vmg8825-api
zyxelclient-vmg8825

ZyxelApiClient

```json
DeviceDiscRespPayload={
   "ApiName": "ZYXEL RESTful API",
   "ModelName": "VMG8825-T50",
   "SoftwareVersion": "V5.50(ABPY.1)b11",
   "DeviceMode": "Router",
   "SupportedApiVersion": [
     {
       "ApiVersion": "1.0",
       "LoginURI": "\/api\/v1\/UserLogin",
       "Protocol": "HTTPS",
       "HttpsPort": 20443
     }
   ],
   "MAC": "08:26:97:DA:DD:80"
 }
```

zyxel VMG8825-T50

https://pypi.org/project/fritzconnection/

```bash
from fritzconnection import FritzConnection

fc = FritzConnection(address='192.168.178.1')
fc.reconnect()  # get a new external ip from the provider
print(fc)  # print router model informations
```

```plain

# file: home_router.yml

- hosts: localhost
  vars:
    zyxel_cli:
      url: "https://192.168.0.1"
      username: "{{ username }}"
      password: "{{ password }}"
  tasks:
    - name: test zyxel
      zyxel_ping:
        name: a
      connection: local

    - name: Zyxel raw command
      zyxel_command:
        provider: "{{ zyxel_cli }}"
          #host
          #port
          controller_baseURL: "https://127.0.0.1:8443"
          controller_username: "admin"
          controller_password: "changeme"
          controller_site: "default"
        method: get
        oid: static_dhcp
      register: result

    - name: debug Zyxel response
      debug:
        mag:

    - name: Configure ipv4 dhcp fixed address
      zyxel_static_dhcp:
        mac: "90:0C:c8:d9:cf:ef"
        ipaddr: 192.168.0.86
        state: present
        enabled: true
        #index: 1
        #brwan: "Default"
        #provider:
        #  host: "{{ inventory_hostname_short }}"
        #  username: admin
        #  password: admin
      connection: local

---
- hosts: localhost
  roles:
    - role: avinetworks.avisdk
  tasks:
    - name: Get login info
      uri:
        url: "https://{{ controller }}/login"
        method: POST
        body:
          username: "{{ username }}"
          password: "{{ password }}"
        validate_certs: no
        body_format: json
      register: login_info
    - name: Get cloud inventory
      avi_api_session:
        avi_credentials:
          username: "{{ username }}"
          password: "{{ password }}"
        controller: "{{ controller }}"
        api_context:
          session_id: "{{ login_info.cookies.sessionid }}"
          csrftoken: "{{ login_info.cookies.csrftoken }}"
        http_method: get
        path: cloud-inventory
      register: cloud_results


      avi_disable_session_cache_as_fact
https://github.com/ansible-collections/community.network/blob/8f08dae3121ea41cc02f62e372b929e208f1c3a0/plugins/module_utils/network/avi/ansible_utils.py
https://github.com/ansible-collections/community.network/blob/8f08dae3121ea41cc02f62e372b929e208f1c3a0/plugins/modules/network/avi/avi_api_version.py


```

## TODO's for unit testing

check test framework files in https://github.com/ansible-collections/ansible.netcommon
check github workflow https://github.com/ansible-collections/collection_template/blob/main/.github/workflows/ansible-test.yml

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
[jwnmulder.zyxel_vmg8825.zyxel_vmg8825](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_vmg8825_httpapi.rst)|Zyxel Web REST interface

### Modules
Name | Description
--- | ---
[jwnmulder.zyxel_vmg8825.zyxel2_facts](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel2_facts_module.rst)|Get facts about zyxel devices.
[jwnmulder.zyxel_vmg8825.zyxel2_static_dhcp](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel2_static_dhcp_module.rst)|Manages <xxxx> attributes of <network_os> <resource>.
[jwnmulder.zyxel_vmg8825.zyxel_dal_raw](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_dal_raw_module.rst)|Zyxel Module
[jwnmulder.zyxel_vmg8825.zyxel_login](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_login_module.rst)|Zyxel Module
[jwnmulder.zyxel_vmg8825.zyxel_logout](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_logout_module.rst)|Zyxel Module
[jwnmulder.zyxel_vmg8825.zyxel_ping](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_ping_module.rst)|Zyxel Module
[jwnmulder.zyxel_vmg8825.zyxel_static_dhcp](https://github.com/jwnmulder/ansible-collection-zyxel-vmg8825/blob/main/docs/jwnmulder.zyxel_vmg8825.zyxel_static_dhcp_module.rst)|Zyxel Module

<!--end collection content-->
