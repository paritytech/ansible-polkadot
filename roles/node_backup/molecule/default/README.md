### Collection 

Molecula should install collection automatically,  If id did not happened run: 
```commandline
mkdir molecule/default/collections
ansible-polkadot collection install -f -r molecule/default/collections.yml -p ./molecule/default/collections
```

### Molecule
#### Docker 
Test role with docker driver 
```shell
molecule create
molecule converge
molecule destroy
```


