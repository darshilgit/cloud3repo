from flask import Flask
import pyodbc as db
import redis

app = Flask(__name__)
conn = db.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:cloud3dbserver.database.windows.net,1433;Database=cloud3db;Uid=dbuser@cloud3dbserver;Pwd={Mypassword!};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
redis_connect_dict = {}
redis_connect_dict['host'] = 'cloud3redis.redis.cache.windows.net'
redis_connect_dict['port'] = 6380
redis_connect_dict['db'] = 0
redis_connect_dict['password'] = 'iMB7hsBunvCnYzZPekiBk+ZAX3TzDKzDplY+Pc8Y2+s='

r = redis.StrictRedis(redis_connect_dict['host'],
                      redis_connect_dict['port'],
                      redis_connect_dict['db'],
                      redis_connect_dict['password'],
                      ssl=True)
@app.route('/')
def hello_world():
    # conn = db.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:cloud3dbserver.database.windows.net,1433;Database=cloud3db;Uid=dbuser@cloud3dbserver;Pwd={Mypassword!};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
    r.set('somekey','value')
    res = r.get('somekey')
    return res
    cursor = conn.cursor()
    cursor.execute('Select count(*) from quakes')
    for row in cursor.fetchall():
        return str(row)
    # if cursor:
    #     print("connected")
    #return 'Hello World from library'


if __name__ == '_main_':
    app.run()


# darshil_parikh@Azure:/usr/local/lib/python2.7/dist-packages$ pip install pyodbc --user
# az webapp config set --resource-group appsvc_rg_Linux_centralus --name cloud3app --linux-fx-version "PYTHON|3.5"