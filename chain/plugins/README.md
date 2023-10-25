# Collections Plugins Directory

This directory can be used to ship various plugins inside an Ansible collection. Each plugin is placed in a folder that
is named after the type of plugin it is in. It can also include the `module_utils` and `modules` directory that
would contain module utils and modules respectively.

Here is an example directory of the majority of plugins currently supported by Ansible:

```
└── plugins
    ├── action
    ├── become
    ├── cache
    ├── callback
    ├── cliconf
    ├── connection
    ├── filter
    ├── httpapi
    ├── inventory
    ├── lookup
    ├── module_utils
    ├── modules
    ├── netconf
    ├── shell
    ├── strategy
    ├── terminal
    ├── test
    └── vars
```

A full list of plugin types can be found at [Working With Plugins](https://docs.ansible.com/ansible/2.10/plugins/plugins.html).

# Filters
## subkey_inspect
Small wrapper around subkey inspect command. 
### Requirements 
Subkey binary should be installed on host machine. 

```bash
curl -fSL -o subkey 'https://releases.parity.io/substrate/x86_64-debian%3Astretch/v3.0.0/subkey/subkey'
chmod +x subkey
sudo mv subkey /usr/local/bin/subkey
subkey -V
```

### Usage
```
{{ var|infrastructure.chain_operations.subkey_inspect(<subkey options>) }}
```

Example:
```
# ./test.yml
- name: test
  hosts: localhost
  gather_facts: false
  vars:
    secretKey: "0xa021a8ab1f9a1b5dd293f56978b64531ec68db5b028197c2577417a24d4fa383//one"
    pubKey: "0x1e3a41ed0424929e949c531654b82baee9869bcea16d1115ca8344b637a44b10"
  tasks:
    - debug:
        msg:
        - "Print all keys:     {{ secretKey | infrastructure.chain_operations.subkey_inspect }}"
        - "Print accountId:    {{ (secretKey | infrastructure.chain_operations.subkey_inspect).accountId }}"
        - "Print publicKey:    {{ (secretKey | infrastructure.chain_operations.subkey_inspect).publicKey }}"
        - "Print secretKeyUri: {{ (secretKey | infrastructure.chain_operations.subkey_inspect).secretKeyUri }}"
        - "Print secretSeed:   {{ (secretKey | infrastructure.chain_operations.subkey_inspect).secretSeed }}"
        - "Print ss58Address:  {{ (secretKey | infrastructure.chain_operations.subkey_inspect).ss58Address }}"
        # call filter with options
        - "Print kusama ss58Address:         {{ (secretKey | infrastructure.chain_operations.subkey_inspect(network='kusama')).ss58Address }}"
        - "Print scheme=Ecdsa ss58Address:   {{ (secretKey | infrastructure.chain_operations.subkey_inspect(scheme='Ecdsa')).ss58Address }}"
        - "Print public key  ss58Address:    {{ (pubKey | infrastructure.chain_operations.subkey_inspect(public=True)).ss58Address }}"
        - "Print public kusama ss58Address:  {{ (pubKey | infrastructure.chain_operations.subkey_inspect(public=True,network='kusama')).ss58Address }}"


# ansible-playbook ./test.yml  --check
**TASK [debug] ******************************************************************************************
ok: [localhost] => {
    "msg": [
        "Print all keys:     {'accountId': '0x1e3a41ed0424929e949c531654b82baee9869bcea16d1115ca8344b637a44b10', 'publicKey': '0x1e3a41ed0424929e949c531654b82baee9869bcea16d1115ca8344b637a44b10', 'secretKeyUri': '0xa021a8ab1f9a1b5dd293f56978b64531ec68db5b028197c2577417a24d4fa383//one', 'secretSeed': '0xf8e0c1c9b22a4e595c0893245c836e9ef235dfea5292e60f85e5c09f823df4cf', 'ss58Address': '5CkLbjyxrLAs8GJNwhaDLtGdhvsFWyS3N6MqSANsz4y37Moi'}",
        "Print accountId:    0x1e3a41ed0424929e949c531654b82baee9869bcea16d1115ca8344b637a44b10",
        "Print publicKey:    0x1e3a41ed0424929e949c531654b82baee9869bcea16d1115ca8344b637a44b10",
        "Print secretKeyUri: 0xa021a8ab1f9a1b5dd293f56978b64531ec68db5b028197c2577417a24d4fa383//one",
        "Print secretSeed:   0xf8e0c1c9b22a4e595c0893245c836e9ef235dfea5292e60f85e5c09f823df4cf",
        "Print ss58Address:  5CkLbjyxrLAs8GJNwhaDLtGdhvsFWyS3N6MqSANsz4y37Moi",
        "Print kusama ss58Address:         DFxG4KqUhBnsv7piQPGEqddrX9VKeFDpUCappeqTsBXrN2H",
        "Print scheme=Ecdsa ss58Address:   5GQUR8Hx2u2KbbUvegJDnyEQGSeLZc6cPK5WWbZ814VsmNV7",
        "Print public key  ss58Address:    5CkLbjyxrLAs8GJNwhaDLtGdhvsFWyS3N6MqSANsz4y37Moi",
        "Print public kusama ss58Address:  DFxG4KqUhBnsv7piQPGEqddrX9VKeFDpUCappeqTsBXrN2H"
    ]
}
```
