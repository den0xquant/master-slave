#!/bin/bash

set -e

cat >> "$PGDATA/pg_hba.conf" <<EOF
host replication all 0.0.0.0/0 md5
EOF