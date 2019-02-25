from flask import Flask, render_template, request
import pyodbc as db
import redis
import pygal
import time

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

line_chart = pygal.Bar()
line_chart.add('a', [1, 2])
line_chart.add('b', [1, 3])


def redis_query(query):
    if r.get(query) == None:
        cursor = conn.cursor()
        rcount = cursor.execute(query).fetchall()
        r.set(query, rcount[0][0])
        return None
    else:
        rcount= r.get(query)
        return rcount
#redisconn()


@app.route('/')
def hello_world():
    # r.set('somekey','value')
    # res = r.get('somekey')
    # return res
    return render_template('common.html')

@app.route('/question1', methods=['GET'])
def query_db():
    return render_template('question1.html', )

@app.route('/question1_execute', methods=['GET'])
def query_db_execute():
    mag = request.args.get('mag')
    oper = request.args.get('oper')
    # if mag != '' and oper != '':


    try:
        # if mag != '' and oper != '':
        cursor = conn.cursor()
        # sql = '''SELECT COUNT(*) FROM QUIZ2TABLE where "mag" < ? '''
        #         # cursor.execute(sql, (mag,))
        sql = "SELECT COUNT(*) FROM quakes where mag " + oper + mag
        if request.args.get('form') == 'Execute':
            startTime = time.perf_counter()
            cursor.execute(sql)
            result = cursor.fetchall()
            endTime = time.perf_counter()
            result = result[0][0]
            total_time = endTime-startTime
        elif request.args.get('form') == 'ExecuteCache':
            startTime = time.perf_counter()
            result = redis_query(sql)
            endTime = time.perf_counter()
            if result != None:
                result = str(result)
                result = result.split('b')
                result = result[-1]
            total_time = endTime - startTime
    except:
        result = "error try again"
    # finally:
    #     conn.close()
    return render_template('question1.html', result=result, total_time=total_time)




if __name__ == '_main_':
    app.run()


# darshil_parikh@Azure:/usr/local/lib/python2.7/dist-packages$ pip install pyodbc --user
# az webapp config set --resource-group appsvc_rg_Linux_centralus --name cloud3app --linux-fx-version "PYTHON|3.5"