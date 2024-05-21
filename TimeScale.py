import psycopg2.extras
import datetime


class TimeScale():
    DB_TABLE = "stocks"
    DB_COLUMNS = ["time", "symbol", "ask_price", "bid_price"]
    MAX_BATCH_SIZE = 100

    def __init__(self):
        self.conn = psycopg2.connect("postgres://tsdbadmin:xzx3ieoq4decawok@g6x9qdc4i3.yuefy52tud.tsdb.cloud.timescale.com:32331/tsdb?sslmode=require")
        self.conn.autocommit = True
        self.current_batch = []
        self.insert_counter = 0

    def insert_row_into_batch(self, row):
        if len(self.current_batch) == self.MAX_BATCH_SIZE - 1:
            self.current_batch.append(row)
            print("batch before appending to db", self.current_batch)
            self.insert_batch_into_db()
        else:
            self.current_batch.append(row)

    def insert_batch_into_db(self):
        if self.conn != None:
            self.insert_counter += 1
            cursor = self.conn.cursor()
            sql_query = f"""INSERT INTO {self.DB_TABLE} ({','.join(self.DB_COLUMNS)}) VALUES %s;"""
            psycopg2.extras.execute_values(cursor, sql_query, self.current_batch)
            self.conn.commit()
            self.current_batch = []

    def get_last_prices(self):
        cursor = self.conn.cursor()
        query = "SELECT ask_price, bid_price FROM stocks ORDER BY time DESC LIMIT 1;"
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row
    
    def get_last_bands(self):
        cursor = self.conn.cursor()
        query = "SELECT upper_band, lower_band FROM bbAgg ORDER BY bucket_time DESC LIMIT 1;"
        cursor.execute(query)
        bands = cursor.fetchone()
        cursor.close()
        return bands
            
            

        


