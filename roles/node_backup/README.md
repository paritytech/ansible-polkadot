node_backup
=========
This role will template out the backup script and the backup Prometheus exporter. Also, it creates the relevant systemd units.<br>
The nodes that we deploy on the same instance, are normal substrate nodes that are syncing the chain.
The backup is made from the local database. These nodes don't have to do any other work other than synchronization.<br>
Nodes are stopped during the backup process of the given chain because otherwise, the database will be changing during 
the backup. It corrupts the backup.
<br><br>
