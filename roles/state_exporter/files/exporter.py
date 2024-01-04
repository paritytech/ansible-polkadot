#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import schedule
import time
import sys
import os
import logging
import traceback
from prometheus_client import start_http_server, Gauge
import psutil

LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

node_chain_folders = {
    'polkadot': 'polkadot',
    'kusama': 'ksmcc3',
    'westend': 'westend2',
    'rococo':  'rococo_v1_12'
}

process_metrics = {
    'polkadot_state_process_cmdline': Gauge(
        'polkadot_state_process_cmdline',
        'cmdline of a node process',
        ['name', 'pid', 'cmd_line']),
    'polkadot_state_process_threads': Gauge(
        'polkadot_state_process_threads',
        'number threads of a node process',
        ['name', 'pid']),
    'polkadot_state_process_memory': Gauge(
        'polkadot_state_process_memory',
        'memory is used by a node process',
        ['name', 'pid']),
    'polkadot_state_process_cpu_percent': Gauge(
        'polkadot_state_process_cpu_percent',
        'memory is used by a node process',
        ['name', 'pid'])
}

node_metrics = {
    'polkadot_state_node_session_key': Gauge(
        'polkadot_state_node_session_key',
        'session key of a node',
        ['name', 'pid', 'session_key'])
}

PORT = 9110


def update_metrics():
    processes = {}

    for proc in psutil.process_iter():
        try:
            process_cmdline = proc.cmdline()
            if not (len(process_cmdline) > 1 and '--name' in process_cmdline and '--chain' in process_cmdline):
                continue
            process_chain = process_cmdline[::-1][process_cmdline[::-1].index('--chain') - 1]
            process_name = process_cmdline[::-1][process_cmdline[::-1].index('--name') - 1]
            process_pid = proc.pid
            process_base_path = process_cmdline[::-1][process_cmdline[::-1].index('--base-path') - 1]\
                if '--base-path' in process_cmdline else None
            # It will delete the previous process if
            # it's the parent of the current process (it can be docker, bash, etc.)
            if process_name in processes and processes[process_name]['pid'] < process_pid:
                del processes[process_name]
            processes[process_name] = {'pid': process_pid,
                                       'chain': process_chain,
                                       'cmd_line': ' '.join(process_cmdline[1:]),
                                       'threads': proc.num_threads(),
                                       'memory': proc.memory_info().rss,
                                       'cpu_percent': proc.cpu_percent(),
                                       'base_path': process_base_path
                                       }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        except Exception as e:
            logger.error(e)
            logger.error(traceback.print_tb(e.__traceback__))
            return
    logger.debug('processes were found: ' + str(processes))

    try:
        # wipe metrics
        for metric in {**process_metrics, **node_metrics}.items():
            for sample in metric[1].collect()[0].samples:
                metric[1].remove(*list(sample.labels.values()))

        for proc in processes:
            process_metrics['polkadot_state_process_cmdline'].labels(
                name=proc,
                pid=processes[proc]['pid'],
                cmd_line=processes[proc]['cmd_line']).set(1)
            process_metrics['polkadot_state_process_threads'].labels(
                name=proc,
                pid=processes[proc]['pid']).set(processes[proc]['threads'])
            process_metrics['polkadot_state_process_memory'].labels(
                name=proc,
                pid=processes[proc]['pid']).set(processes[proc]['memory'])
            process_metrics['polkadot_state_process_cpu_percent'].labels(
                name=proc,
                pid=processes[proc]['pid']).set(processes[proc]['cpu_percent'])
            if processes[proc]['base_path']:
                keystore_path = os.path.join(
                    processes[proc]['base_path'],
                    'chains',
                    node_chain_folders[processes[proc]['chain']],
                    'keystore')
                node_session_key = parse_session_key(keystore_path)
                if node_session_key:
                    node_metrics['polkadot_state_node_session_key'].labels(
                        name=proc,
                        pid=processes[proc]['pid'],
                        session_key=node_session_key).set(1)
    except Exception as e:
        logger.error(e)
        logger.error(traceback.print_tb(e.__traceback__))
        return


def parse_session_key(dir):
    # variants of key prefixes in the right order
    key_formats = (
        ['6772616e', '62616265', '696d6f6e', '70617261', '61756469'], # v1 validator keys (gran,babe,imon,para,audi)
        ['6772616e', '62616265', '696d6f6e', '70617261', '6173676e', '61756469'], # v2 validator keys (gran,babe,imon,para,asgn,audi)
        ['6772616e', '62616265', '696d6f6e', '70617261', '6173676e', '61756469', '62656566'], # v3 validator keys (gran,babe,imon,para,asgn,audi,beef)
        ['61757261'] # collator keys (aura)
    )
    possible_prefixes = list(set([j for i in key_formats for j in i]))
    if os.path.isdir(dir):
        os.chdir(dir)
        files = os.listdir('.')
        files = [i for i in files if len(i) in [72, 74] and i[0:8] in possible_prefixes]
        if not files:
            return None
        # find creation time of the newest key
        time_of_last_key = sorted(list(set([int(os.path.getmtime(i)) for i in files])))[-1]
        # parse the newest public keys and prefix them with the names of files.
        # make sure to only pick up the keys created within 60 seconds interval
        keys = {i[0:8]: i[8:] for i in files if int(os.path.getmtime(i)) <= time_of_last_key and int(os.path.getmtime(i)) > time_of_last_key - 60}
        logger.debug('keys were found: ' + str(keys) + ' in the keystore path: ' + dir)
        for key_format in key_formats:
            if set(keys.keys()) == set(key_format):
                # build the session key
                session_key = '0x' + ''.join([keys[i] for i in key_format])
                logger.debug('the session key was parsed: ' + session_key + ' in the keystore path: ' + dir)
                return(session_key)
        logger.error('Error parsing the session key')
    return None


if __name__ == '__main__':
    global logger
    logger = logging.getLogger('state_exporter')

    # console handler
    ch = logging.StreamHandler()
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    formatter = logging.Formatter(LOGGING_FORMAT)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Start up the server to expose the metrics
    start_http_server(PORT)  # Metrics server
    schedule.every(10).seconds.do(update_metrics)
    while True:
        schedule.run_pending()
        time.sleep(1)
