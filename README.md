# Ansible Collection - paritytech.chain_operations

## Install Ansible collections

Create `requirements.yml` file in your playbook repository (or add to the existing file):
```yaml
collections:
  - name: https://github.com/paritytech/ansible-galaxy.git
    type: git
    version: main
```

If you want to install collections in the project space, you have to run:
```commandline
mkdir collections
ansible-galaxy collection install -f -r requirements.yml -p ./collections
```

If you want to install collections in the global space (`~/.ansible/collections`),
you have to run:
```commandline
ansible-galaxy collection install -f -r requirements.yml
```

## Roles

Node role - [README](./roles/node/README.md) 
