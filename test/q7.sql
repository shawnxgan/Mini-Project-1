-- Get information about an order
select deliveries.trackingno as trackingNo, orders.oid as oid, deliveries.pickUpTime as pickUpTime, deliveries.dropOffTime as dropOffTime, orders.address as address
FROM orders, deliveries
where 7 == orders.oid and orders.oid == deliveries.oid;




--deliveries(trackingno, oid, pickUpTime, dropOffTime)
