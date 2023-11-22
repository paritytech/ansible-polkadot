### Molecule
#### Docker 
Test role with docker driver 
```shell
molecule create
molecule converge
molecule verify
molecule destroy
```

#### LXD 
Test role with LXD driver 
```shell
DRIVER=lxd molecule create
DRIVER=lxd molecule converge
DRIVER=lxd molecule verify
DRIVER=lxd molecule destroy
```
