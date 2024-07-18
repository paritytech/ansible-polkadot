# Ansible Polkadot Collection - paritytech.chain

## Install Ansible collections

Create `requirements.yml` file in your playbook repository (or add to the existing file):
```yaml
collections:
  - name: https://github.com/paritytech/ansible-polkadot.git
    type: git
    version: 1.10.0
```

or

```yaml
collections:
  - name: paritytech.chain
    version: 1.10.0
```

If you want to install collections in the project space, you have to run:
```commandline
mkdir collections
ansible-polkadot collection install -f -r requirements.yml -p ./collections
```

If you want to install collections in the global space (`~/.ansible/collections`),
you have to run:
```commandline
ansible-polkadot collection install -f -r requirements.yml
```

## Roles

* key_inject - [README](./roles/key_inject/README.md)
* node - [README](./roles/node/README.md)
* node_backup - [README](./roles/node_backup/README.md)
* secure_apt - [README](./roles/secure_apt/README.md)
* state_exporter - [README](./roles/state_exporter/README.md)
* ws_health_exporter - [README](./roles/ws_health_exporter/README.md)
* nginx - [README](./roles/nginx/README.md)
* nginx_exporter - [README](./roles/nginx_exporter/README.md)
