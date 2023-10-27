# Parity Ansible Collections

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

### chain
key_inject - [README](chain/roles/key_inject/README.md)  
node - [README](chain/roles/node/README.md)  
node_backup - [README](chain/roles/node_backup/README.md)  
state_exporter - [README](chain/roles/state_exporter/README.md)  
ws_health_exporter - [README](chain/roles/ws_health_exporter/README.md)

### common
secure_apt - [README](common/roles/secure_apt/README.md)