
Glossary
--------

Trade Message: A trade message is a message containing trade information. It has at
least order type, quantity, price, side, client order id.

Order: An order is the latest state of a sequence of transactions.


References
----------

https://www.onixs.biz/fix-dictionary/4.2/msgs_by_msg_type.html


Design
------


The system read a list of trade message dump files and rebuild the state of
transactions.


### Data Structure

We consider below order type in our application:
- 8: Execution Report
- 9: Order Cancel Reject
- D: New Order - Single
- F: Order cancel request
- G: Order cancel/Replace request


Below we define the execution report.
```
MsgType	OrderID	ClOrdID	OrigClOrdID	ExecID	ExecType	OrdStatus	Symbol	Side	LeavesQty	CumQty	AvgPx	TransactTime
```

Below we define the order cancel reject.
```
MsgType	OrderID	ClOrdID	OrdStatus	TransactTime
```

Below we define the new order single.
```
MsgType	ClOrdID	Symbol	Side	TransactTime	OrderQty	OrdType	Price
```

Below we define the order cancel request.
```
MsgType	OrigClOrdID	ClOrdID	Symbol	Side	TransactTime
```

Below we define the order cancel/replace request.
```
MsgType	OrigClOrdID	ClOrdID	Symbol	Side	TransactTime	OrderQty	OrdType	Price
```


### Fields

Side:
	1 = Buy
	2 = Sell

OrdType:
	1 = Market
	2 = Limit

OrdStatus:
	0 = New
	1 = Partially filled
	2 = Filled
	3 = Done For Day
	4 = Canceled
	5 = Replaced
	6 = Pending Cancel
	8 = Rejected

ExecType:
	0 = New
	1 = Partial Fill
	2 = Fill
	3 = Done For Day
	4 = Canceled
	5 = Replaced
	6 = Pending Cancel
	7 = Stopped
	8 = Rejected
	9 = Suspended
	A = Pending New
	B = Calculated
	C = Expired
	D = Restarted
	E = Pending Replace

### Workflow


- Orders are stored in files in the order in which they are received.
- Every file has a process to which reads the order and convert in the format
defined above.
- All streams are merged in a single stream by a multiplexer.
- In parallel
	+ Stream 1
		- Message stream per order is saved in a file. One file per order.
	+ Stream 2
		- Track the last state of all orders based on the message stream.
		- Save orders. One file per order.
	+ Stream 3
		- Save a ClOrdId mapping in a file.


### Folder Structure


- work_folder
	+ orders
		- ClOrdID.1
		- ClOrdID.2
		- ClOrdID.3
	+ order_stream
		- ClOrdID.1
		- ClOrdID.2
		- ClOrdID.3
	+ cl_ord_id_map
		- ClOrdID.1
		- ClOrdID.2
		- ClOrdID.3

### Queries

We need below queries:
- Search order by ClOrdID.
- Search order stream by ClOrdID.
- Search orders by Symbol
- Filter orders by TransactTime
- Filter orders by OrderStatus
- Order orders by TransactTime
- Filter messages by MsgType


### Order Status Definition

- isCanceled -> 'canceled'
- qty == filledQty -> 'filled'
- replaceStack.last.msgType == cancel -> 'pending_cancel'
- replaceStack.last.msgType == replace -> 'pending_replace'
- qty == 0 -> 'new'
- default -> 'partially_filled'


