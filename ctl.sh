#!/bin/bash

run_server() {
    
    echo "packages time" > $4
    python3 $1.server.py --host $2 --port $3 2>&1 | tee >(grep --line-buffered "Finished processing client" | awk -F ' ' '{print $4, $8; fflush()}' >> $4)
}


while [[ $# -gt 0 ]]; do
    case $1 in
        "--mode")
            mode=$2
            shift 2
            ;;
        "--host")
            host=$2
            shift 2
            ;;
        "--port")
            port=$2
            shift 2
            ;;
        "--out")
            out=$2
            shift 2
            ;;
    esac
done

run_server $mode $host $port $out
