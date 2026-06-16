#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
matlab -nodesktop -batch "run('${SCRIPT_DIR}/run_tests.m')"
