# Substrate node deployment ansible role

The role can deploy a Substrate node.

There are available relaychain roles: `validator`, `boot`, `full` and `rpc`.
There are available parachain roles: `collator`, `validator`, `rpc` and `full`.
 
The role can work in `check mode` regardless of the current state of the infrastructure.
Use `--diff --check` CLI parameters to test changes before applying. 

## Role preferences


You can find all available variables and comments in the `defaults/main.yml` file.
Almost all default values of variables do not need to be changed.
You can redefine common or some very specific variables in your playbooks
or inventory files if you need.

You can find all available variables in the `vars/main.yml` file.

## Requirements

* You have to be able to use `become`
* The role can't be run with default values of variables only. You have to specify the `node_chain` variable
  at least.

## Examples

### Wipe block storage before deploying

`ansible-playbook --tags "node" -e "node_database_wipe=true" -e "node_parachain_database_wipe=true" playbook.yml`

```yaml
- hosts: host1
  become: yes
  roles:
    - node
  vars:
    node_database_wipe: true
    node_parachain_database_wipe: true
```

### Restart nodes only

`ansible-playbook --tags "node" -e "node_binary_deployment=False"
-e "node_systemd_deployment=False" -e "node_force_restart=True" playbook.yml`

```yaml
- hosts: host1
  become: yes
  roles:
    - node
  vars:
    node_binary_deployment: false
    node_systemd_deployment: false
    node_force_restart: true
```

## Contributing

If you want to add functionality or change something, please, try to save backward compatibility.
A lot of playbook can be dependent on the role. Breaking changes should
be discussed in a common review.

## Chain IDs

The list doesn't contain all possible IDs and can be outdated.

Relaychain chain IDs:
```yaml
polkadot: "polkadot"
kusama: "ksmcc3"
westend: "westend2"
rococo:  "rococo_v2_2"
rococo-local: "rococo_local_testnet"
```

Parachain chain IDs:
```yaml
statemine: "statemine"
statemint: "statemint"
westmint: "westmint"
```

## Example basic inventory

```
all:
  vars:
    node_app_name: company-chain
    node_binary_version: v0.9.29
    node_chain: rococo-local
    node_user: polkadot
    node_binary: https://github.com/paritytech/polkadot/releases/download/{{ node_binary_version }}/polkadot
    node_binary_signature: https://github.com/paritytech/polkadot/releases/download/{{ node_binary_version }}/polkadot.asc
  children:
    validators:
      vars:
      hosts:
        validator1:
          node_custom_options: ["--alice"]
          ansible_host: validator1.company.com
          node_role: validator
        validator2:
          node_custom_options: ["--bob"]
          ansible_host: validator2.company.com
          node_role: validator
    rpcs:
        rpc1:
          ansible_host: rpc1.company.com
          node_role: rpc
    collators:
      vars:
        node_binary: https://github.com/paritytech/cumulus/releases/download/{{ node_binary_version }}0/polkadot-parachain
        node_binary_signature: https://github.com/paritytech/cumulus/releases/download/{{ node_binary_version }}0/polkadot-parachain.asc
        node_parachain_chain: shell
      hosts:
        collator1:
          ansible_host: collator1.company.com
          node_parachain_role: collator
```
