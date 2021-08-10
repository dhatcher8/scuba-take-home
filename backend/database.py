from config import DB_Host, DB_Name, DB_Password, DB_Port, DB_Username
import psycopg2
import psycopg2.extras

class DBConnection():

    def __init__(self):
        self.CONNECTION = "dbname =" + DB_Name + " user=" + DB_Username + " password=" + DB_Password + " host=" + DB_Host + " port=" + DB_Port + " sslmode=require"

    def getAll(self):
        with psycopg2.connect(self.CONNECTION) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * from eod_stock_prices;")
            values = cursor.fetchall()
            return values

    def dataExists(self, stock_symbol, start_date, end_date):
        with psycopg2.connect(self.CONNECTION) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * from eod_stock_prices where symbol = '" + stock_symbol + "' and dt = '" + start_date + "';")
            print(cursor.fetchall())
            if len(cursor.fetchall()) > 0:
                cursor.execute("SELECT * from eod_stock_prices where symbol = '" + stock_symbol + "' and dt = '" + end_date + "';")
                print(cursor.fetchall())
                if len(cursor.fetchall()) > 0:
                    return True;
            return False;

    def deleteData(self, stock_symbol):
        with psycopg2.connect(self.CONNECTION) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE from eod_stock_prices where symbol = '" + stock_symbol + "';")

    def getData(self, stock_symbol, start_date, end_date):
        with psycopg2.connect(self.CONNECTION) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * from eod_stock_prices where symbol = '" + stock_symbol + "' and dt >= '" + start_date + "' and dt <= '" + end_date + "';")
            data = cursor.fetchall()
            print(data)
            return(data)

    def addData(self, data_to_add):
        with psycopg2.connect(self.CONNECTION) as conn:
            cursor = conn.cursor()
            insert_query = 'INSERT INTO eod_stock_prices (symbol, dt, price) values %s'
            psycopg2.extras.execute_values (
                cursor, insert_query, data_to_add, template=None, page_size=100
            )

    def getQuartiles(self, stock_symbol, start_date, end_date):
        with psycopg2.connect(self.CONNECTION) as conn:
            cursor = conn.cursor()
            # cursor.execute("SELECT PERCENTILE_CONT(0.0, 0.25, 0.5, 0.75, 1.0) WITHIN GROUP (ORDER BY (eod_stock_prices.price)) from eod_stock_prices")
            data = cursor.fetchall()
            print(data)
            return(data)

    def startDateExists(self):
        pass

    def getLastExistingDate(self):
        pass
