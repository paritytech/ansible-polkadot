#!/usr/bin/python

# Copyright: (c) 2022, Devops Parity <devops@parity.io>
# GPL-2.0-or-later
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sudo_schedule_para_initialize
short_description: Schedule a para to be initialized at the start of the next session.
version_added: "0.0.1"
description: 
  - Schedule a para to be initialized at the start of the next session by using sudo account.
  - This module is wrapper for substrate-interface python library.
  - Only for testnets, requires SUDO.
requirements:
  - substrate-interface
options:
    url:
        description: WS rpc endpoint.
        required: true
        type: str
    key:
        description: Key to  commit transaction. 
        required: true
        type: str
    key_type: 
        description: Key type hex seed or uri
        required: false
        type: choices=['seed', 'uri']
        default: 'seed'
    id:
        description: Para Id
        required: true
        type: int
    genesis_head: 
        description: Head data for a Para Id
        required: true
        type: bool
    validation_code:
        description: Validation code for a Para Id.
        required: true
        type: str
    parachain:
        description: parachain
        required: false
        type: bool
        default: true
    state:
        description: Whether to onboard (present), or cleanup (absent) a parachain.
        required: false
        type: choices=['present', 'absent']
        default: 'present'
        
author:
    - Bulat Saifullin (@BulatSaif)
'''

EXAMPLES = r'''
# Register parachain id 1000
- name: Register parachain 
  infrastructure.chain_operations.sudo_schedule_para_initialize:
    url: 'ws://127.0.0.1:9944'
    key: "//Alice"
    key_type: uri
    id: "1000"
    genesis_head: "0x41"
    validation_code: "0x1111"
    
# use key hex seed 
- name: Register parachain 
  infrastructure.chain_operations.sudo_schedule_para_initialize:
    url: 'ws://127.0.0.1:9944'
    key: "0x56...92"
    id: "1000"
    genesis_head: "{{ lookup('file', 'path/to/genesis-state') }}"
    validation_code: "{{ lookup('file', 'path/to/genesis-wasm') }}"

'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
receipt:
    description: Receipt returned by substrate-interface
    returned: always
    type: complex
    contains:
        block_hash:
            description: 
              - block_hash where extrinsic is included, you can use it in polkadot.js.org
              - Example: https://polkadot.js.org/apps/#/explorer/query/0xc3c238e11de1e0e74ca076b002934d437a4c5a044cdc91cf7835c09f82a941d6
            type: str
            returned: always
            sample: '0xc3c238e11de1e0e74ca076b002934d437a4c5a044cdc91cf7835c09f82a941d6'
        error_message:
            description: Returns the error message if the extrinsic failed in format
            type: dict
            returned: always
            sample: {'type': 'System', 'name': 'BadOrigin', 'docs': 'Bad origin'}
        extrinsic_hash:
            description: Extrinsic hash
            type: str
            returned: always
            sample: '0xf9b9acd0dcb6cead3db84cb1046350df148e2a9ab9494e9da8ab894a43c2b115'
        extrinsic_idx:
            description: Retrieves the index of this extrinsic in containing block
            type: int
            returned: always
            sample: 4
        finalized:
            description: Is finalized
            type: bool
            returned: always
            sample: false
        is_success:
            description: 
              - Returns True if ExtrinsicSuccess event is triggered, 
              - False in case of ExtrinsicFailed In case of False error_message will contain more details about the error
            type: bool
            returned: always
            sample: true
        total_fee_amount:
            description: 
              - Contains the total fee costs deducted when executing this extrinsic. 
              - This includes fee for the validator ( (Balances.Deposit event) and the fee deposited for the treasury (Treasury.Deposit event)
            type: int
            returned: always
            sample: 54907300087520         
        weight:
            description: Contains the actual weight when executing this extrinsic
            type: int
            returned: always
            sample: 11000
        triggered_events:
            description: 
              - Gets triggered events for submitted extrinsic. block_hash where extrinsic is included is required, 
              - manually set block_hash or use wait_for_inclusion when submitting extrinsic
            type: List
            returned: always
            sample: [
              {"attributes":["5FeyRQmjtdHoPH56ASFW76AJEP1yaQC1K9aEMvJTF9nzt9S9",54907300087520],"event":{"attributes":["5FeyRQmjtdHoPH56ASFW76AJEP1yaQC1K9aEMvJTF9nzt9S9",54907300087520],"event_id":"Withdraw","event_index":"0408","module_id":"Balances"},"event_id":"Withdraw","event_index":4,"extrinsic_idx":4,"module_id":"Balances","phase":"ApplyExtrinsic","topics":[]},
              {"attributes":["0x0b004419ddaed13fd1f08044685597485b1054e61ea2d293346205fea0d6d500",524],"event":{"attributes":["0x0b004419ddaed13fd1f08044685597485b1054e61ea2d293346205fea0d6d500",524],"event_id":"PvfCheckStarted","event_index":"1305","module_id":"Paras"},"event_id":"PvfCheckStarted","event_index":19,"extrinsic_idx":4,"module_id":"Paras","phase":"ApplyExtrinsic","topics":[]},
              {"attributes":["0x0b004419ddaed13fd1f08044685597485b1054e61ea2d293346205fea0d6d500",524],"event":{"attributes":["0x0b004419ddaed13fd1f08044685597485b1054e61ea2d293346205fea0d6d500",524],"event_id":"PvfCheckAccepted","event_index":"1306","module_id":"Paras"},"event_id":"PvfCheckAccepted","event_index":19,"extrinsic_idx":4,"module_id":"Paras","phase":"ApplyExtrinsic","topics":[]},
              {"attributes":{"Ok":[]},"event":{"attributes":{"Ok":[]},"event_id":"Sudid","event_index":"2000","module_id":"Sudo"},"event_id":"Sudid","event_index":32,"extrinsic_idx":4,"module_id":"Sudo","phase":"ApplyExtrinsic","topics":[]},
              {"attributes":["5FeyRQmjtdHoPH56ASFW76AJEP1yaQC1K9aEMvJTF9nzt9S9",54907300087520],"event":{"attributes":["5FeyRQmjtdHoPH56ASFW76AJEP1yaQC1K9aEMvJTF9nzt9S9",54907300087520],"event_id":"Deposit","event_index":"0407","module_id":"Balances"},"event_id":"Deposit","event_index":4,"extrinsic_idx":4,"module_id":"Balances","phase":"ApplyExtrinsic","topics":[]},
              {"attributes":{"class":"Operational","pays_fee":"Yes","weight":11000},"event":{"attributes":{"class":"Operational","pays_fee":"Yes","weight":11000},"event_id":"ExtrinsicSuccess","event_index":"0000","module_id":"System"},"event_id":"ExtrinsicSuccess","event_index":0,"extrinsic_idx":4,"module_id":"System","phase":"ApplyExtrinsic","topics":[]}
              ]
parachain:
    description: Receipt returned by substrate-interface
    returned: always
    type: complex
    contains:
        currentCodeHash:
            description: Current wasm hash in network for ParaId
            type: str
            returned: always
            sample: "0x0b004419ddaed13fd1f08044685597485b1054e61ea2d293346205fea0d6d500"
        paraLifecycles:
            description: Current state of parachain
            type: str
            returned: always
            sample: "Parachain"
'''

import traceback
from ansible.module_utils.basic import AnsibleModule

try:
    from substrateinterface import SubstrateInterface, Keypair
    from substrateinterface.exceptions import SubstrateRequestException
    from substrateinterface.utils.hasher import blake2_256

    python_substrateinterface_installed = True
except ImportError:
    python_substrateinterface_installed = False


def test_dependencies(module):
    if not python_substrateinterface_installed:
        module.fail_json(msg="substrate-interface required for this module. see TODO link to this file")


def test_genesis(module):
    try:
        genesis_bytearray = bytearray.fromhex(module.params['genesis_head'].replace('0x', ''))
    except ValueError as e:
        module.fail_json(msg="genesis_head is not hex, Error: %s" % e, exception=traceback.format_exc())

    try:
        code_bytearray = bytearray.fromhex(module.params['validation_code'].replace('0x', ''))
    except ValueError as e:
        module.fail_json(msg="validation_code is not hex, Error: %s" % e, exception=traceback.format_exc())

    return "0x" + blake2_256(code_bytearray)


def check_parachain_exists(module, substrate):
    para_id = module.params['id']
    para_lifecycles = substrate.query('Paras', 'ParaLifecycles', params=[para_id])
    para_current_code_hash = substrate.query('Paras', 'CurrentCodeHash', params=[para_id])

    return {'paraLifecycles': para_lifecycles.value, 'currentCodeHash': para_current_code_hash.value}


def get_substrate(module):
    try:
        substrate = SubstrateInterface(
            url=module.params['url'],
        )
    except ConnectionRefusedError as e:
        module.fail_json(msg="Unable to connect to Substrate node url: %s, Error: %s " % (module.params['url'], e))

    system_health = substrate.rpc_request(method="system_health", params=[])
    if system_health["result"]["isSyncing"]:
        module.fail_json(msg="Node '%s', is syncing" % (module.params['url'],))

    return substrate


def get_keypair(module):
    if module.params['key_type'] == 'seed':
        try:
            keypair = Keypair.create_from_seed(module.params['key'])
        except ValueError as e:
            module.fail_json(msg="Error parsing key seed: %s" % e, exception=traceback.format_exc())
    elif module.params['key_type'] == 'uri':
        try:
            keypair = Keypair.create_from_uri(module.params['key'])
        except ValueError as e:
            module.fail_json(msg="Error parsing key uri: %s" % e, exception=traceback.format_exc())
    else:
        module.fail_json(msg="key_type: %s, is not supported" % module.params['key_type'])
    return keypair


def add_parachain(module, substrate, keypair):
    payload = substrate.compose_call(
        call_module='ParasSudoWrapper',
        call_function='sudo_schedule_para_initialize',
        call_params={
            'id': module.params['id'],
            'genesis': {
                'genesis_head': module.params['genesis_head'],
                'validation_code': module.params['validation_code'],
                'parachain': module.params['parachain']
            }
        }
    )

    call = substrate.compose_call(
        call_module='Sudo',
        call_function='sudo',
        call_params={
            'call': payload.value,
        }
    )

    extrinsic = substrate.create_signed_extrinsic(
        call=call,
        keypair=keypair,
    )

    try:
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        return receipt
    except SubstrateRequestException as e:
        module.fail_json(msg="Failed to send Request: %s" % e, exception=traceback.format_exc())


def cleanup_parachain(module, substrate, keypair):
    payload = substrate.compose_call(
        call_module='ParasSudoWrapper',
        call_function='sudo_schedule_para_cleanup',
        call_params={
            'id': module.params['id']
        }
    )

    call = substrate.compose_call(
        call_module='Sudo',
        call_function='sudo',
        call_params={
            'call': payload.value,
        }
    )

    extrinsic = substrate.create_signed_extrinsic(
        call=call,
        keypair=keypair,
    )

    try:
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        return receipt
    except SubstrateRequestException as e:
        module.fail_json(msg="Failed to send Request: %s" % e, exception=traceback.format_exc())


def parse_receipt_and_exit(module, substrate, result, receipt):
    result['receipt'] = {
        'block_hash': receipt.block_hash,
        'error_message': receipt.error_message,
        'extrinsic_hash': receipt.extrinsic_hash,
        'extrinsic_idx': receipt.extrinsic_idx,
        'finalized': receipt.finalized,
        'is_success': receipt.is_success,
        'total_fee_amount': receipt.total_fee_amount,
        'weight': receipt.weight,
        'triggered_events': [event.value for event in receipt.triggered_events]
    }
    result['parachain'] = check_parachain_exists(module, substrate)

    if module._diff:
        result['diff']['after'] = result['parachain']

    if result['receipt']['is_success']:
        for event in receipt.triggered_events:
            if "Err" in event.value["attributes"]:
                module.fail_json(msg='Triggered event failed: %s' % event.value["attributes"], **result)
        module.exit_json(**result)
    else:
        module.fail_json(
            msg='Transaction is not successful: https://polkadot.js.org/apps/?rpc=%s#/explorer/query/%s'
                % (module.params['url'], result['receipt']['block_hash']), **result)


def run_module():
    module_args = dict(
        url=dict(type='str', default='ws://127.0.0.1:9944'),
        key=dict(type='str', required=True),
        key_type=dict(choices=['seed', 'uri'], default='seed'),
        id=dict(type='int', required=True),
        genesis_head=dict(type='str'),
        validation_code=dict(type='str'),
        parachain=dict(type='bool', default=True),
        state=dict(choices=['present', 'absent'], default='present'),
    )

    required_if = [
        ('state', 'present', ('genesis_head', 'validation_code')),
    ]

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=required_if
    )

    result = dict(
        changed=False
    )

    test_dependencies(module)

    substrate = get_substrate(module)

    keypair = get_keypair(module)

    parachain_state = check_parachain_exists(module, substrate)

    result['parachain'] = dict(parachain_state)

    if module.params['state'] == 'present':

        new_parachain_code_hash = test_genesis(module)
        result['parachain'].update({'newCodeHash': new_parachain_code_hash})

        if module._diff:
            result['diff'] = {
                "before": parachain_state,
                "after": {'paraLifecycles': "Parachain", 'currentCodeHash': new_parachain_code_hash},
            }

        if not parachain_state['paraLifecycles'] or parachain_state['currentCodeHash'] != new_parachain_code_hash:
            result['changed'] = True
        else:
            # parachain is registered and parachain_code match, exit here
            module.exit_json(**result)

        # if it is the check mode, exit here
        if module.check_mode:
            module.exit_json(**result)

        receipt = add_parachain(module, substrate, keypair)
        parse_receipt_and_exit(module, substrate, result, receipt)

    else:
        if module._diff:
            result['diff'] = {
                "before": parachain_state,
                "after": {'paraLifecycles': None, 'currentCodeHash': None},
            }
        if parachain_state['paraLifecycles']:
            result['changed'] = True
        else:
            # parachain is not registered exit here
            module.exit_json(**result)

        # if it is the check mode, exit here
        if module.check_mode:
            module.exit_json(**result)

        receipt = cleanup_parachain(module, substrate, keypair)
        parse_receipt_and_exit(module, substrate, result, receipt)


def main():
    run_module()


if __name__ == '__main__':
    main()
