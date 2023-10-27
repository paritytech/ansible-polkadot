#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pickle
import json
import logging
import threading
import traceback
import io
from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server, Gauge


LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


cache_filename = os.path.dirname(__file__) + '/exporter.cache'

backup_labels = ['id', 'storage', 'bucket_name', 'service_name', 'version']
backup_metrics = {
    "timestamp":    Gauge('node_backup_timestamp',
                          'Time of the last backup (unix timestamp)',
                          backup_labels),
    "size":         Gauge('node_backup_size',
                          'Size of the last backup (byte)',
                          backup_labels),
    "last_block":   Gauge('node_backup_last_block',
                          'Last block in the last backup (byte)',
                          backup_labels),
    "last_backup":  Gauge('node_backup_last_backup',
                          'Last backup',
                          backup_labels + ['backup_name', 'tar_backup_path', 'backup_path']),
    "total_size":   Gauge('node_backup_total_size',
                          'Size of all backups (byte)',
                          ['storage', 'bucket_name'])
}


def update_cache(key, value):
    if os.path.exists(cache_filename) and os.path.getsize(cache_filename) > 0:
        with open(cache_filename, 'rb') as f:
            data = pickle.load(f)
    else:
        data = {}
    data[key] = value
    with open(cache_filename, 'wb') as f:
        pickle.dump(data, f)


def fetch_cache():
    if os.path.exists(cache_filename) and os.path.getsize(cache_filename) > 0:
        with open(cache_filename, 'rb') as f:
            data = pickle.load(f)
            logging.info(f"Fetched from cache: {data}")
            return data
    else:
        return {}


def clean_metrics(id, backup_name, version):
    """
    Purge records with old versions
    """

    def check_record(key_value) -> bool:
        return (
                id in key_value['labels'] and
                key_value['name'] != 'node_backup_total_size' and
                (
                    (key_value['name'] == 'node_backup_last_backup' and backup_name not in key_value['labels']) or
                    version not in key_value['labels']
                )
        )

    for metric in backup_metrics.items():
        current_metrics=[{'name': i.name, 'labels': list(i.labels.values()), 'value': i.value} for i in metric[1].collect()[0].samples]
        old_metrics = list(filter(check_record, current_metrics))
        for old_metric in old_metrics:
            logging.info(f"clean {old_metric['name']} metric with label set: {str(old_metric['labels'])}")
            metric[1].remove(*old_metric['labels'])


def set_metrics(data):
    id = f"{data['storage']}-{data['bucketName']}-{data['serviceName']}"
    common_labels={'id': id,
                   'storage': data['storage'],
                   'bucket_name': data['bucketName'],
                   'service_name': data['serviceName'],
                   'version': data['version']}
    if  data['bucketDomain'] != '':
        backup_path=f"https://{data['bucketDomain']}/{data['serviceName']}/{data['backupName']}"
        tar_backup_path=f"https://{data['bucketDomain']}/tar/{data['serviceName']}/{data['backupName']}.tar"
    elif data['bucketDomain'] == '' and data['storage'] == 'gcp':
        backup_path=f"gs://{data['bucketName']}/{data['serviceName']}/{data['backupName']}"
        tar_backup_path=f"https://storage.googleapis.com/{data['bucketName']}/tar/{data['serviceName']}/{data['backupName']}.tar"
    else:
        raise Exception("'bucketDomain' has to be defined")
    clean_metrics(id, data['backupName'], data['version'])
    backup_metrics['timestamp'].labels(**common_labels).set(int(data['timeStamp']))
    backup_metrics['size'].labels(**common_labels).set(int(data['size']))
    backup_metrics['last_block'].labels(**common_labels).set(int(data['lastBlock']))
    backup_metrics['last_backup'].labels(**common_labels,
                                         backup_name=data['backupName'],
                                         backup_path=backup_path,
                                         tar_backup_path=tar_backup_path).set(1)
    backup_metrics['total_size'].labels(storage=data['storage'],
                                        bucket_name=data['bucketName']).set(int(data['totalSize']))
    update_cache((data['storage'], data['bucketName'], data['serviceName']), data)
    logging.info(f"request was processed successfully. data: {data}")


class HttpProcessor(BaseHTTPRequestHandler):
    """
    HTTP Server
    """
    BaseHTTPRequestHandler.server_version = 'Python API'

    def log_message(self, format, *args):
        message = f"{self.address_string()} {format % args}"
        logging.info(message)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()


    def do_POST(self):
        if self.headers.get('Content-Type') != 'application/json':
            self.send_error(400, "Only application/json supported")
            self.end_headers()
            return
        data = ""
        try:
            # read the message and convert it into a python dictionary
            length = int(self.headers['content-length'])
            data = self.rfile.read(length)

            set_metrics(json.loads(data))
            self.send_response(200)

            self._set_headers()
            self.wfile.write(json.dumps({"status": "OK"}).encode("utf8"))
        except json.decoder.JSONDecodeError as e:
            tb_output = io.StringIO()
            traceback.print_tb(e.__traceback__, file=tb_output)
            logging.error(f"JSON decoding error. error: '{e}', JSON: '{data}'")
            logging.error(f"JSON decoding error. traceback:\n{tb_output.getvalue()}")
            tb_output.close()
            self.send_error(400, 'JSONDecodeError')
            return
        except Exception as e:
            tb_output = io.StringIO()
            traceback.print_tb(e.__traceback__, file=tb_output)
            logging.error(f"request processing error. error: '{e}'")
            logging.error(f"request processing error. traceback:\n{tb_output.getvalue()}")
            tb_output.close()
            self.send_error(500)
            return


def start_servers():
    """
    Start HTTP Servers
    """
    # Start up the server to expose the metrics.
    start_http_server(9109)  # Metrics server
    server_address = ('127.0.0.1', 60101)  # Data reception server
    server = HTTPServer(server_address, HttpProcessor)
    server.serve_forever()


if __name__ == '__main__':

    # set up console log handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter(LOGGING_FORMAT)
    console.setFormatter(formatter)
    # set up basic logging config
    logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO, handlers=[console])


    for backup in fetch_cache().items():
        try:
            set_metrics(backup[1])
        except KeyError as e:
            logging.error(f"cache fetching error. error: {e}, key: {backup[0]}, value: {backup[1]}")
        except Exception as e:
            tb_output = io.StringIO()
            traceback.print_tb(e.__traceback__, file=tb_output)
            logging.error(f"cache fetching error. error: '{e}'")
            logging.error(f"cache fetching error. traceback:\n{tb_output.getvalue()}")
            tb_output.close()
            sys.exit(1)

    thread = threading.Thread(target=start_servers, args=())
    thread.daemon = True
    thread.start()
    thread.join()
