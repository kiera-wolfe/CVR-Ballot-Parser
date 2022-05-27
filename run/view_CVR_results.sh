#!/bin/bash
type bokeh &>/dev/null || {
    echo 'bokeh not found!'
    echo 'Install using the following command:'
    echo -e '\tpip install --user bokeh'
    exit 1
} >&2

run() {
    local THIS_PATH="$(dirname "$0")"
    local REPO_ROOT="$THIS_PATH/.."

    echo "The code repository is at $(realpath "$REPO_ROOT")"
    
    # print the welcome text
    cat < "$THIS_PATH/welcome.txt"
    echo

    # print the config text
    cat < "$THIS_PATH/config.txt"
    echo

    # run the bokeh server
    local RUN_FILE="$REPO_ROOT/src/display.py"
    echo "Running the bokeh server with $RUN_FILE"

    # $1 = repository root directory
    # $2 = configuration file path
    # $3 = CVR directory path
    bokeh serve \
	  --show "$RUN_FILE" \
	  --args "$REPO_ROOT" 'run' 'run/cvr'
}

run "$@"
