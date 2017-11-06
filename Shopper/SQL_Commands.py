import sqlite3

class SQLCommands:
    def __init__(self, conn, cursor):
        self.__conn = conn;
        self.__curs = cursor;

    def checkAvailableCid(self, cid):
        result = self.__curs.execute("""SELECT * FROM customers WHERE cid == ?;""", (cid,))
        result = result.fetchall()
        if len(result) == 0:
            return True;
        else:
            return False; # Username already exists
    
    def customerLogin(self, cid, password):
        # print(cid, password)
        # Validate a customer's login credentials.
        result = self.__curs.execute("""SELECT * FROM customers WHERE cid == ? AND pwd == hash(?);""", (cid, password,))
        result = result.fetchall()
        # print(result)
        if len(result) > 0 and result[0][0] == cid:
            return True;
        else:
            return False;
    
    def agentLogin(self, aid, password):
        # print(cid, password)
        # Validate a customer's login credentials.
        result = self.__curs.execute("""SELECT * FROM agents WHERE aid == ? AND pwd == hash(?);""", (aid, password,))
        result = result.fetchall()
        # print(result)
        if len(result) > 0 and result[0][0] == aid:
            return True;
        else:
            return False;
    
    def registerCustomer(self, cid, name, address, pwd):
        # Returns a boolean indicating success of registration
        try:
            self.__curs.execute("""INSERT INTO customers VALUES(?,?,?,hash(?));""", (cid, name, address, pwd,))
            return True;
        except:
            False;  


    def search(self, queryString):
        # Searches based on assignment specifications.
        # Returns [(pid, name, unit, carriedBy, inStockAt, cheapestEver, cheapestAvailable, recentOrders), ...]
        # Expect query to be a comma delimited string
        queries = [ x.strip() for x in queryString.split(",")]

        while "" in queries:
            queries.remove("")
        
        # Create the query string.
        matchTemplate = "SELECT pid, name, unit FROM products WHERE name like ?"
        matchString = '('
        numQueries = len(queries)

        if numQueries == 0:
            return None; # No results found.

        for i in range(0, numQueries):
            keyword = queries[i]
            # print(i, keyword, len(keyword))
            if i == numQueries - 1:
                # For the last item
                matchString += matchTemplate  + ")"
            else:
                matchString += matchTemplate + " UNION ALL "

        # Send query.
        search_query = """(SELECT pid, name, unit FROM """ + matchString + """ GROUP BY pid ORDER BY count(*) DESC)"""
        big_query = """
            SELECT stats.pid, name, unit, carriedBy, inStockAt, cheapestEver, cheapestAvailable, recentOrders FROM \
            (SELECT search.pid, name, unit, \
            count(*) as carriedBy,\
            sum(case when qty > 0 THEN 1 ELSE 0 END) as inStockAt,\
            min(uprice) as cheapestEver, \
            min(case when qty > 0 THEN uprice ELSE NULL END) as cheapestAvailable FROM """ + search_query + """\
            search, carries \
            WHERE search.pid == carries.pid\
            GROUP BY search.pid\
            HAVING MIN(uprice)) as stats LEFT OUTER JOIN (\
                select pid, sum(qty) as recentOrders from orders, olines\
                where orders.oid == olines.oid and date("now") <= date(orders.odate, "+7 day")\
                group by pid\
            ) as sortedOrders on stats.pid = sortedOrders.pid;"""
        result = None;
        try:
            result = self.__curs.execute(big_query, tuple(["%" + x + "%" for x in queries]))
            result = result.fetchall()
        except:
            print("failed to execute search!")
            return None; # Failed to run query;
        
        return result
        # print("Result:",result)
    
    def getProductInfo(self, pid):
        # Returns detailed information about availability of a product.
        pid = str(pid)
        big_query = """select info.pid, info.name, info.unit, info.cat, info.sid, info.storeName, info.uprice, info.qty from\
        (select products.pid, products.name, products.unit, products.cat, stores.sid, stores.name as storeName, carries.uprice, carries.qty, (CASE WHEN carries.qty > 0 THEN 1 ELSE 0 END) as switch\
        from products, carries, stores\
        where products.pid == ? and products.pid == carries.pid and stores.sid == carries.sid\
        order by uprice asc) as info\
        order by switch desc;"""

        result = None
        try:
            result = self.__curs.execute(big_query, (pid,))
            result = result.fetchall()
        except:
            print("Failed to get product info")
            return None;
        
        return result;
    
    def getInvalidItems(self, basket):
        # Returns any items that exceed what's in stock from basket
        # Basket is a list: [(pid,sid,qty,uprice), ...]
        # Assumes unique (pid, sid)
        # Returns [(sid, pid, qty, uprice) ...]

        areInvalid = None
        # If greater than quantity, returns it so we can ask customer to input it again
        query_Template = """SELECT * FROM carries where sid == ? and pid == ? and ? > qty"""
        query_String = ""

        args_List = []
        for i in range(0, len(basket)):
            item = basket[i]
            args_List.append(item[2]) # Add sid
            args_List.append(item[1]) # Add pid
            args_List.append(item[3]) # Add qty

            if i == len(basket) - 1:
                # For the last element, don't add union all
                query_String += query_Template
            else:
                query_String += query_Template + """ UNION ALL """
        query_String += ";"

        # Check for any items with order qty > in stock
        result = None
        try:
            self.__curs.execute(query_String, tuple(args_List));
            result = self.__curs.fetchall()
        except:
            print("Error in validating order")
            return None
        
        if len(result) > 0:
            print("Some invalid items valid")
            # Customer requested more items than in stock at that store
        return result;

    def placeOrder(self, cid, address, basket):
        # Basket is a list: [(pid,sid,qty,uprice,), ...]
        # Assumes all items are valid

        #Get order number, oid is int so we can +1 for this order
        oid = 0;
        try:
            maxOid = self.__curs.execute("""SELECT MAX(oid) FROM orders;""")
            oid = maxOid.fetchone()[0]
            oid += 1;
        except:
            print("Failed to get last order")
            return False;
        
        # Add to orders table
        self.__curs.execute("""INSERT INTO orders(?,?,date("now"),?);""", (oid, cid, address))
        
        insertions = []

        # Add to insertions
        for item in basket:
            # olines(oid, sid, pid, qty, uprice)
            insertValue = (oid, item[1], item[0], item[2], item[3])
            insertions.append(insertValue)

        # Add items from basket to olines
        try:
            self.__curs.executemany("""INSERT INTO olines VALUES(?, ?, ?, ?, ?);""", insertions)
        except:
            print("FAILED TO CREATE ORDER")
            return False;
            
        return True;

    def listOrders(self, cid):
        # List all orders made by the customer
        # Returns [(oid, odate, numberOfProducts, totalPrice, orderDate,), ...]

        query_String = """select orders.oid as oid, orders.odate as odate, count(DISTINCT olines.pid) as numberOfProducts, SUM(olines.uprice) as totalPrice, orders.odate as orderDate\
        FROM orders, olines\
        WHERE orders.oid == olines.oid AND orders.cid == ?\
        group by orders.oid\
        order by orders.odate DESC;"""

        results = None;
        try:
            results = self.__conn.execute(query_String, (cid,))
            results = results.fetchall()
            return results
        except:
            print("Failed to fetch queries")
            return None;

    def getOrderInfo(self, oid):
        # Gets required information about a specific order
        # Return order: [(trackingNo, oid, pickUpTime, dropOffTime, address,), ...]

        query_String = """select deliveries.trackingno as trackingNo, orders.oid as oid, deliveries.pickUpTime as pickUpTime, deliveries.dropOffTime as dropOffTime, orders.address as address\
        FROM orders, deliveries\
        where orders.oid == ? and orders.oid == deliveries.oid;"""

        result = None;
        try:
            result = self.__curs.execute(query_String, (oid,))
            result = result.fetchall();
            return result;
        except:
            print("Error in getting order info")
            return None;
        
    def listOrderItems(self, oid):
        # Returns items listing in an order
        # Return order: [(sid, storeName, pid, name, qty, unit, uprice,), ...]

        query_String = """select olines.sid as sid, stores.name as storeName, olines.pid as pid, products.name as name, olines.qty as qty, products.unit as unit, olines.uprice as uprice\
        from olines, stores, products\
        where olines.oid == ? and olines.sid == stores.sid and olines.pid == products.pid;"""

        result = None;
        try:
            result = self.__curs.execute(query_String, (oid,))
            result = result.fetchall()
            return result;
        except:
            print("Error in fetching item listing");
            return None;

    
    # Agent interface
    def setupDelivery(self, addOrdersInfo):
        # addOrdersInfo: [(oid, pickUpTime, dropOffTime,),...]
        # time is in SQL format ("+8 day".. etc)

        #Get order number, oid is int so we can +1 for this order
        oid = 0;
        try:
            maxTrackingNo = self.__curs.execute("""SELECT MAX(trackingno) FROM deliveries;""")
            maxTrackingNo = maxTrackingNo.fetchone()[0]
            maxTrackingNo += 1;
        except:
            print("Failed to get last trackignNo")
            return False;
        
        try:
            self.__curs.executemany("""INSERT INTO deliveries VALUES(?, date(?), date(?);""", addOrdersInfo)
            return True;
        except:
            return False;
    
    def removeOrderFromDelivery(self, trackingNo, oid):
        # Removes order from a delivery
        # Returns bool indicating success

        query_String = """DELETE FROM deliveries\
        WHERE deliveries.trackingno = ? AND deliveries.oid = ?;"""

        try:
            self.__curs.execute(query_String, (trackingNo, oid,))
            return True;
        except:
            print("Failed to delete order from deliveries")
            return False;
    
    def listDeliveryItems(self, trackingNo):
        # List items from a delivery
        # Returns [(oid, customer, odate, address, pickUpTime, dropOffTime,),...]

        query_String = """select orders.oid as oid, customers.name as customer, orders.odate as odate, orders.address as address, deliveries.pickUpTime as pickUpTime, deliveries.dropOffTime as dropOffTime\
        FROM deliveries, orders, customers\
        WHERE deliveries.trackingno == ? and deliveries.oid == orders.oid and customers.cid == orders.cid;"""

        result = None;

        try:
            result = self.__curs.execute(query_String, (trackingNo,))
            result = result.fetchall()
            return result;
        except:
            print("Failed to list delivery items")
            return False;
    
    def updateOrder(self, trackingNo, order, pickUpTime, dropOffTime):
        # Updates an order's pickUp/dropOff Time
        # pickup time and dropOffTime are sql like dates: "+7 day", "+2 day" .. etc
        # Returns bool, whether update was successful or not 

        query_String = """UPDATE deliveries \
        SET deliveries.pickUpTime = date(?), deliveries.dropOffTime = date(?) \
        WHERE deliveries.trackingNo == ? AND deliveries.order == ?"""

        try:
            self.__curs.execute(query_String, (pickUpTime, dropOffTime, trackingNo, order,))
            return True;
        except:
            return False;

    def addToStock(self, sid, pid, qty, uprice):
        query_String = """INSERT INTO carries VALUES(?, ?, ?, ?)"""

        try:
            self.__curs.execute(query_String, (sid, pid, qty, uprice,));
            return True;
        except:
            return False;

# from DB_Make import *
# conn = sqlite3.connect('../test/demo.db')
# curs = conn.cursor()
# conn.create_function("hash", 1, encrypt)
# sqc = SQLCommands(conn, curs);

# # Update order
# sqc.updateOrder(9, 8, "now")

# print(sqc.getOrderInfo(10))
# print(sqc.listOrderItems(7))

# print(sqc.registerCustomer("12345", "DevonThe tester", "5678", "PWD"))

# conn.commit()
# conn.close()
# # Test login
# print(sqc.customerLogin('c1','davood'))


# searchResults = sqc.search("coffee")
# print(searchResults)
# for productInfo in searchResults:
#     print(sqc.getProductInfo(productInfo[0]))

# basket = [('c1', 'p1', 1, 20),
#           ('c1', 'p2', 2, 80),
#          ]
# isValid = sqc.getInvalidItems(basket)
# print(isValid)
# sqc.placeOrder([])
