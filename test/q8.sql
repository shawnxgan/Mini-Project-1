-- Get item listings from an order

select olines.sid as sid, stores.name as name, olines.pid as pid, products.name as name, olines.qty as qty, products.unit as unit, olines.uprice as unitprice
from olines, stores, products
where olines.oid == 1 and olines.sid == stores.sid and olines.pid == products.pid;