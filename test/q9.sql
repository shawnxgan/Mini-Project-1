-- Get infoList about products in a delivery

select orders.oid as oid, customers.name as customer, orders.odate as odate, orders.address as address, deliveries.pickUpTime as pickUpTime, deliveries.dropOffTime as dropOffTime
FROM deliveries, orders, customers
WHERE deliveries.trackingno == 1 and deliveries.oid == orders.oid and customers.cid == orders.cid;