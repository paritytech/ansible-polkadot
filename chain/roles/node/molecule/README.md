## Ansible molecule test
[Molecule](https://molecule.readthedocs.io/en/latest/) allow us to apply and test roles. 
Molecule will create instances (platforms) using a selected driver (e.g. docker, vagrant, azure, gcp...).
Then it will apply role, test it (verify.yml) and clean everything.

### Requirements 
- yamllint
- ansible-lint
- molecule

**Install:**
```bash
sudo su 
apt install -y  yamllint
pip3 install 'molecule[docker]' ansible-lint
```
**Check:**
```bash
$ yamllint --version; ansible-lint --version; molecule --version;
yamllint 1.20.0
ansible-lint 5.3.0 using ansible 2.11.6
molecule 3.5.2 using python 3.8 
    ansible:2.11.6
    delegated:3.5.2 from molecule
    docker:1.1.0 from molecule_docker requiring collections: community.docker>=1.9.1
```

### Test role
#### Relaychain
```bash
cd roles/node
molecule test
```
#### Parachain
```bash
cd roles/node
molecule test  -s parachain
```


### Deploy locally
You can deploy role locally in docker container, e.g to check node logs.
#### Relaychain
```bash
cd roles/node
molecule lint
molecule converge
molecule verify
molecule login
> journalctl -f
> exit
molecule destroy # to clean everything
```
#### Parachain
```bash
cd roles/node
molecule lint
molecule converge --scenario-name parachain
molecule verify --scenario-name parachain
molecule login --scenario-name parachain --host instance-parachain 
> journalctl -f
> exit
molecule destroy --scenario-name parachain # to clean everything
```