from flask import Flask, render_template, request
import pyodbc as db
import redis
import pygal
import time
import random

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
        # sql = '''SELECT COUNT(*) FROM QUIZ2TABLE where "mag" < ? '''
        #         # cursor.execute(sql, (mag,))
        sql = "SELECT COUNT(*) FROM quakes where mag " + oper + mag
        if request.args.get('form') == 'no':
            startTime = time.perf_counter()
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            endTime = time.perf_counter()
            result = result[0][0]
            total_time = endTime-startTime
        elif request.args.get('form') == 'yes':
            startTime = time.perf_counter()
            result = redis_query(sql)
            endTime = time.perf_counter()
            if result != None:
                result = str(result)
                result = result.replace("'",'')
                result = result.split('b')
                result = result[-1]
            total_time = endTime - startTime
    except:
        result = "error try again"
    # finally:
    #     conn.close()
    return render_template('question1.html', result=result, total_time=total_time)


@app.route('/question2', methods=['GET'])
def query_db_2():
    return render_template('question2.html', )

@app.route('/question2_execute', methods=['GET'])
def query_db_2_execute():
    qcount = request.args.get('qcount')
    qcount = int(qcount)
    lmag = float(request.args.get('lmag'))
    hmag = float(request.args.get('hmag'))
    try:
        if request.args.get('form') == 'no':
            startTime = time.perf_counter()
            while qcount != 0:
                sql = "SELECT COUNT(*) FROM quakes where mag =" + str(round(random.uniform(lmag, hmag), 1))
                cursor = conn.cursor()
                result = cursor.execute(sql).fetchall()
                qcount = qcount - 1
            endTime = time.perf_counter()
            total_time = endTime - startTime
        elif request.args.get('form') == 'yes':
            startTime = time.perf_counter()
            while qcount != 0:
                sql = "SELECT COUNT(*) FROM quakes where mag =" + str(round(random.uniform(lmag, hmag), 1))
                result = redis_query(sql)
                qcount = qcount - 1
            endTime = time.perf_counter()
            total_time = endTime - startTime
    except:
        result = "error try again"
    return render_template('question2.html', total_time=total_time)

@app.route('/question3', methods=['GET'])
def question3():
    return render_template('question3.html',)

@app.route('/question3_execute', methods=['GET'])
def question3_execute():
    year = str(request.args.get('year'))
    year = 'y_' + year
    stc = request.args.get('stc')
    try:
        #startTime = time.perf_counter()
        # while qcount != 0:
        sql = "SELECT population."+ year + " FROM population INNER JOIN statecode on population.State = statecode.state where state_code =" + "'" +str(stc)+"'"
        print(sql)
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        #qcount = qcount - 1
        #endTime = time.perf_counter()
        #total_time = endTime - startTime
    except:
        result = "error try again"
    return render_template('question3.html', result=result)



@app.route('/question4', methods=['GET'])
def question4():
    return render_template('question4.html',)

@app.route('/question4_execute', methods=['GET'])
def question4_execute():
    # year = str(request.args.get('year'))
    # year = 'y_' + year
    stc = request.args.get('stc')

    try:
        #startTime = time.perf_counter()
        # while qcount != 0:
        sql = "select count(county), counties.state from counties INNER JOIN statecode on counties.state = statecode.state where state_code = " + "'"+ str(stc) + "'" + " GROUP BY counties.state"
        sql2 = "select counties.county from counties inner join statecode on counties.state = statecode.state where statecode.state_code = " + "'"+ str(stc) + "'"
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()
        result2 = cursor.execute(sql2).fetchall()
        print(result2)
        #qcount = qcount - 1
        #endTime = time.perf_counter()
        #total_time = endTime - startTime
    except:
        result = "error try again"
    return render_template('question4.html', result=result, result2 = result2)

@app.route('/question5', methods=['GET'])
def question5():
    return render_template('question5.html',)

@app.route('/question5_execute', methods=['GET'])
def question5_execute():
    year = str(request.args.get('year'))
    year = 'y_' + year
    lpop = str(request.args.get('lpop'))
    hpop = str(request.args.get('hpop'))
    print(year)
    print(lpop)
    print(hpop)
    try:
        #startTime = time.perf_counter()
        # while qcount != 0:
        sql = "select population."+ year +" from population where " + year + " BETWEEN" + "'" +lpop + "'" + " and " "'" + hpop + "'"
        print(sql)
        cursor = conn.cursor()
        result = cursor.execute(sql).fetchall()

        #qcount = qcount - 1
        #endTime = time.perf_counter()
        #total_time = endTime - startTime
    except:
        result = "error try again"
    return render_template('question5.html', result=result)

@app.route('/clear_redis_execute', methods=['GET'])
def clear_redis_execute():
    r.flushdb()
    print('flushed')
    return render_template('question2.html')
if __name__ == '_main_':
    app.run()


# darshil_parikh@Azure:/usr/local/lib/python2.7/dist-packages$ pip install pyodbc --user
# az webapp config set --resource-group appsvc_rg_Linux_centralus --name cloud3app --linux-fx-version "PYTHON|3.5"
# SELECT population.y_2010, population.State
# FROM population
# INNER JOIN statecode
# ON population.State = statecode.state
# WHERE state_code = 'CA';

# SELECT population.y_2010
# FROM population
# INNER JOIN counties on counties.state = population.State
# WHERE counties.state = 'California' and counties.county='San Francisco'
