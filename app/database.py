import sqlite3

#connection = sqlite3.connect("sqlite.db")

#cursor = connection.cursor()

#cursor.execute("""
#                CREATE TABLE IF NOT EXISTS shipment (
#                id INTEGER PRIMARY KEY AUTOINCREMENT, 
#                content TEXT,
#                weigh REAL,
#                status TEXT)
#               """)

#cursor.execute("""
#                INSERT INTO shipment (content, weigh, status)
#                VALUES ('Books', 2.5, 'IN_TRANSIT')
#            """)

#cursor.execute("""
#            INSERT INTO shipment 
#            VALUES (NULL, "BOOK 2", 1.0, "PENDING")
#            """)


#shipment = cursor.execute("""
#            SELECT * FROM shipment
#""")
#print(shipment.fetchall())
#print(shipment.fetchone())
#print(shipment.fetchmany(1))

#cursor.execute("""
#    UPDATE shipment SET status='DELIVERED' WHERE id=1
#""")

#cursor.execute("""
#    DELETE FROM shipment where id=2
#""")
#cursor.connection.commit()

#cursor.execute("""
#    DROP TABLE shipment
#""")
#cursor.connection.commit()

#cursor.connection.commit()
#connection.close()