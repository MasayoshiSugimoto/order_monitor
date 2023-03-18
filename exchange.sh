#!/bin/bash


readonly WORK_FOLDER='/mnt/c/temp/exchange'
readonly ORDER_BOOK="${WORK_FOLDER}/order-book"

# Order book format
# sell|price|buy
# 0|90|0
# 10|80|0
# 1|70|0
# 0|60|10
# 0|50|20


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


function generate_order {
	awk '
		BEGIN {
			 for (;;) {
				 print("1 2 3 4")
				 fflush()
			 }
		}
	'
}


function render_messages {
	python3 -c '
from src.message_util import asHumanTable
asHumanTable()
	' \
		| column -t -s'	' 
}



mkdir -p $WORK_FOLDER

while getopts "hlsdr" arg; do
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
		*)
			echo "ERROR: Bad arguments."
			echo "usage"
			exit 1
  esac
done

