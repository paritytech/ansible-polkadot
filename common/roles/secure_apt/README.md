Role Name
=========

A role to apply an APT repository + key securely as the apt_key Ansible module is deprecated

Requirements
--------------

* You have to be able to use `become`

Example Playbook
----------------

  - hosts: servers  
    roles:
      - paritytech.common.secure_apt  
    vars:
      secure_apt_key: B53DC80D13EDEF05  
      secure_apt_repositories:
        - https://packages.cloud.google.com/apt cloud-sdk-{{ ansible_distribution_release }} main
