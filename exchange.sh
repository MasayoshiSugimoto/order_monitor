#!/bin/bash


readonly WORK_FOLDER="/dev/shm/${USER}/exchange"
readonly ORDER_BOOK="${WORK_FOLDER}/order-book"
readonly CL_ORD_ID_MAP_FOLDER="${WORK_FOLDER}/cl_ord_id_map"
readonly ORDER_ID_MAP_FOLDER="${WORK_FOLDER}/order_id_map"
readonly ORDER_ID_MAP_FIFO="${WORK_FOLDER}/order_id_map_fifo"
readonly CL_ORD_ID_MAP_FIFO="${WORK_FOLDER}/cl_ord_id_map_fifo"


function get_field {
    local field_number=$1
    cut -d'|' -f${field_number}
}


function fatal {
    local text="$1"
    echo "ERROR: $text"
    exit 1
}


function consume_orders {
    local book=()
    local side='buy'
    local price=0
    local quantity=0
    local buy_quantity=0
    local sell_quantity=0

    while read -r line; do
        side=$(echo $line | get_field 1)
        price=$(echo $line | get_field 2)
        quantity=$(echo $line | get_field 3)

        sell_quantity=$(echo ${book[price]} | get_field 1)
        if [ -z "${sell_quantity}" ]; then
            sell_quantity=0
        fi

        buy_quantity=$(echo ${book[price]} | get_field 2)
        if [ -z "${buy_quantity}" ]; then
            buy_quantity=0
        fi

        if [ $side == 'buy' ]; then
            buy_quantity=$((buy_quantity + quantity))
        elif [ $side == 'sell' ]; then
            sell_quantity=$((sell_quantity + quantity))
        else
            fatal "Invalid side: $side"
        fi
        book[price]="${sell_quantity}|${buy_quantity}"
    done

    echo "SELL|PRICE|BUY"
    for price in ${!book[@]}; do
        sell_quantity=$(echo ${book[price]} | get_field 1)
        buy_quantity=$(echo ${book[price]} | get_field 2)
        echo "${sell_quantity}|${price}|${buy_quantity}"
    done
}


function render_messages {
	python3 -c '
from src.message_util import asHumanTable
asHumanTable()
	' \
		| column -t -s'	' 
}


function generate_clOrdID_map {
	python3 -c '
from src.services.clOrdID_map_manager import generateClOrdIDMap
generateClOrdIDMap()
'
}


function generate_orderID_map {
	python3 -c '
from src.services.orderID_map_manager import generateOrderIDMap
generateOrderIDMap()
'
}


function save_map {
	local folder="$1"
	while read line; do
		local key=$(echo $line | cut -f1 | base64)
		local file="$folder/$key"
		if ! [[ -f "$file" ]]; then
			echo "$line" > $file
		fi
	done
}


function sort_message {
	python3 -c '
from src.services.message_sorter import sortMessages
sortMessages()
'
}


function generate_messages {
	python3 -c '
from src.services.message_generator import generateMessages
generateMessages()
'
}


rm -rf $WORK_FOLDER
mkdir -p $WORK_FOLDER
mkdir -p $CL_ORD_ID_MAP_FOLDER
mkdir -p $ORDER_ID_MAP_FOLDER
mkfifo $CL_ORD_ID_MAP_FIFO
mkfifo $ORDER_ID_MAP_FIFO

while getopts "hlsdrtg" arg; do
  case $arg in
    h)
      echo "usage" 
			exit 0
      ;;
    l)
			list_commits
			exit 0
      ;;
		s)
			commit_stat_by_user
			exit 0
			;;
		d)
			list_diff_size
			exit 0
			;;
		r)
			render_messages
			exit 0
			;;
		t)
			$(cat $ORDER_ID_MAP_FIFO | generate_clOrdID_map | save_map "$CL_ORD_ID_MAP_FOLDER") &
			$(cat $CL_ORD_ID_MAP_FIFO | generate_orderID_map | save_map "$ORDER_ID_MAP_FOLDER") &
			tee $ORDER_ID_MAP_FIFO \
				| tee $CL_ORD_ID_MAP_FIFO \
				| sort_message \
				| render_messages
			exit 0
			;;
		g)
			generate_messages
			exit 0
			;;
		*)
			echo "ERROR: Bad arguments."
			echo "usage"
			exit 1
  esac
done

