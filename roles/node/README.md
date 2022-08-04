# Polkadot node deployment ansible role

The role can deploy a Polkadot node.

There are available chains: `polkadot`, `kusama`, `westend`.

There are available modes: `validator`, `boot`, `rpc`.
 
The role can work in `check mode` regardless of the current state of the infrastructure.
Use `--diff --check` CLI parameters to test changes before applying. 

## Role preferences

A Polkadot validator node will be deployed by default.

You can find all available variables and comments in the `defaults/main.yml` file.
Almost all default values of variables do not need to be changed.
You can redefine common or some very specific variables in your playbooks
or inventory files if you need.

You can find all available variables in the `vars/main.yml` file.

## Requirements

* You have to be able to use `become`
* You must have a user. The node will be ran by the user using its permissions
* You have to set the `node_user_home_path` variable using the user's home directory path

## Examples

### Wipe block storage before deploying

`ansible-playbook --tags "node" -e "node_force_wipe=true" playbook.yml`

```yaml
- hosts: host1
  become: yes
  roles:
    - node
  vars:
    node_force_wipe: true
```

### Restore block storage during deployment

`ansible-playbook --tags "node" -e "node_restore_chain=true" playbook.yml`

```yaml
- hosts: host1
  become: yes
  roles:
    - node
  vars:
    node_restore_chain: true
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
