from flask import Flask
import pyodbc as db
import redis

app = Flask(__name__)


@app.route('/')
def hello_world():
    conn = db.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:cloud3dbserver.database.windows.net,1433;Database=cloud3db;Uid=dbuser@cloud3dbserver;Pwd={Mypassword!};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")

    cursor = conn.cursor()
    cursor.execute('Select count(*) from quakes')
    for row in cursor.fetchall():
        print(row)
    # if cursor:
    #     print("connected")
    return 'Hello World from library'


if __name__ == '_main_':
    app.run()
