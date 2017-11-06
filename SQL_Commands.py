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
            self.__curs.execute(""""INSERT INTO customers(?,?,?,hash(?));""", (cid, name, address, pwd,))
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
            
        
        
        # Generate output

        
from DB_Make import *
conn = sqlite3.connect('../demo.db')
curs = conn.cursor()
conn.create_function("hash", 1, encrypt)
sqc = SQLCommands(conn, curs);

print(sqc.registerCustomer("1234", "Devon", "5678", "PWD"))


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
