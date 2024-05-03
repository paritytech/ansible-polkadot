# key_inject ansible role

This Ansible role is designed to facilitate the injection of cryptographic keys
into Polkadot nodes, a crucial step for setting up a node for active
participation in network operations like consensus and block authoring. This is
meant only for development and testing purposes and use is not recommended in 
production.

## Key Role Functionality
The `key_inject` role consists of several tasks organized into specific YAML
files to streamline the process of key management on a Polkadot node:

### Key Tasks and Files
- **check_session_key.yml**: Checks whether session keys are present in the
  node’s keystore.
- **inject.yml**: Manages the injection of keys that are not found in the
  keystore.
- **main.yml**: Coordinates the flow between checking and injecting keys.

### Detailed Process
1. **Key Generation**:
   - Generates session keys from specified private keys using
   `paritytech.chain.subkey_inspect`, defaulting to the `sr25519` cryptographic
   scheme.

2. **Key Verification**:
   - An RPC call checks for the presence of keys in the keystore. If absent,
   the process retries up to 12 times, with a 10-second pause between each try.

3. **Key Injection**:
   - If keys are missing in the keystore, they are injected via an RPC call.
   This includes handling for errors and notifications for service restarts
   after successful injections.

4. **Results Reporting**:
   - Outcomes of the injection process are logged, indicating the success or
   failure of the key injections.

### Security and Risk Considerations
Using Ansible for key management is feasible but must be approached with caution,
particularly on networks with real economic value:
- **Secure Storage**: Keys should be encrypted and securely stored within
  Ansible variables. Use `ansible-vault encrypt` for sensitive data.
- **Unique Keys**: Ensure no key sharing across nodes to avoid risks like
  slashing.

**Risk of Slashing**: There's a high risk of slashing in production if keys are
mismanaged, particularly from issues like double-signing due to key reuse.

**Best Practice**: In production environments, the use of `author_rotateKeys`
RPC method is strongly recommended over manual methods to mitigate risks.
This method ensures keys are managed securely, preventing equivocation.
If `author_rotateKeys` is not utilized, consider implementing robust key
management server software that provides safeguards against key misuse and 
equivocation.

## Usage Instructions
```bash
# playbooks/inject_keys.yaml
---
- name: Inject keys into Polkadot nodes
  hosts: polkadot
  gather_facts: false
  tasks:
    - name: Inject keys
      ansible.builtin.include_role:
        name: paritytech.chain.key_inject
```
```bash
# group_vars/polkadot.yaml
subkey_path: "https://releases.parity.io/substrate/x86_64-debian:stretch/v3.0.0/subkey/subkey"
key_inject_relay_chain_rpc_port: 9944
key_inject_relay_chain_key_list:
  - scheme: "sr25519"
    type: "gran"
    priv_key: "0xcc...9123//1//grandpa"
  - type: "babe"
    priv_key: "SECRET SEED"
  - type: "imon"
    priv_key: "SECRET SEED"
  - type: "para"
    priv_key: "SECRET SEED"
  - type: "asgn"
    priv_key: "SECRET SEED"
  - type: "audi"
    priv_key: "SECRET SEED"
key_inject_check_session_key: true
```

## Additional Resources
This role supports a structured approach to key management but should only be
used with a clear understanding of the security requirements and potential
consequences like [slashing for equivocation](https://wiki.polkadot.network/docs/maintain-guides-avoid-slashing#equivocation).
For further details on cryptographic practices in Polkadot, visit
[Cryptography on Polkadot](https://wiki.polkadot.network/docs/learn-cryptography).
