#!/bin/bash
#
# Script for generating and comparing filesystem snapshots

SNAPSHOTS_FOLDER="snapshots"

generate_baseline(){

	local ip="$1"
	local username="$2"
	local baseline_filename="$SNAPSHOTS_FOLDER/$ip-baseline.log"

	ssh "$username"@"$ip" 'bash' < scripts/create_snapshot.sh >\
 "$baseline_filename"

	echo "[+] The baseline snapshot was created."

}

compare_actual_with_baseline(){

	local ip="$1"
	local username="$2"
	local date=$(date +%s)
	local baseline_filename="$SNAPSHOTS_FOLDER/$ip-baseline.log"

	# Check if the baseline snapshot exists
	if [ ! -f "$baseline_filename" ]
	then
		echo "[!] The baseline file for this machine does not exists!"
		exit 1
	fi

	# Create a new snapshot
	local actual_filename="$SNAPSHOTS_FOLDER/$ip-$date.log"
	ssh "$username"@"$ip" 'bash' < scripts/create_snapshot.sh >\
 "$actual_filename"

	# Compare the baseline snapshot with the new one
	python3 scripts/compare_snapshots.py "$baseline_filename" "$actual_filename"

}

main(){

	# Check if the snapshot folder exists
	if [ ! -d "$SNAPSHOTS_FOLDER" ]
	then
		mkdir $SNAPSHOTS_FOLDER
		echo "[+] The snapshots folder was created."
	else
		echo "[i] The snapshots folder already exists."
	fi

	# Check and get the parameters
	if [ "$#" -ne 3 ]; then
		echo -e "[!] Usage: $0 ACTION IP USERNAME\n    ACTION can be \"baseline\
\" for baseline generation/updating or \"compare\" for comparing the baseline\
 snapshot with actual one." >&2
		exit 1
	fi
	local action="$1"
	local ip="$2"
	local username="$3"

	# Execute the action
	if [ "$action" == "baseline" ]
	then
		generate_baseline "$ip" "$username"
	elif [ "$action" == "compare" ]
	then
		compare_actual_with_baseline "$ip" "$username"
	fi

}

main "$@"