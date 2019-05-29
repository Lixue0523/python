#print "====================Python DB-API======================="
#print "reference link: http://www.runoob.com/python/python-mysql.html "
#print "link: https://pynative.com/python-postgresql-tutorial/"
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import getpass
#print "Handle Erro-  InternalError: CREATE DATABASE cannot run inside a transaction block"
print "Please provider Database information which you want to clear dbs and users for Suite installation ~"
host = raw_input("Server host: ")
port = raw_input("Port: ")
database = raw_input("Db: ")
username = raw_input("Username: ")
pwd = getpass.getpass("Password: ")
dbList = ['maas_admin', 'maas_template', 'xservices_ems', 'xservices_mng', 'xservices_rms', 'sxdb','bo_ats', 'bo_user', 'bo_config','bo_license','smartadb','idm','autopassdb']
userList = ['maas_admin','bo_db_user','smartaidm','autopass']

#dbList = ['lxDB1','lxDB2']
#userList = ['lxUser1','lxUser2']
try:
    conn = psycopg2.connect( database = database, user = username, password = pwd, host = host, port = port)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    print "Connect to database successfully!"
    cur = conn.cursor()
    cur.execute('SELECT version();')
    record = cur.fetchone()
    print "You are connected to - ",record,"\n"
    print "===========Prepare to clear DBs ==============="
    for dbName in dbList:
        sqlQ='SELECT * from pg_database where datname = \'%s\'' %(dbName)
        print "Executing commands: ", sqlQ
        cur.execute(sqlQ)
        if bool(cur.rowcount):
            print "DB %s exists" %(dbName)
            sqlT="SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity  WHERE datname='%s' AND pid<>pg_backend_pid();" %(dbName)
            sqlD = "DROP database \"%s\";" %(dbName)
            print "Executing commands: ", sqlT
            cur.execute(sqlT)
            print "Executing commands: ", sqlD
            cur.execute(sqlD)
            print "Database %s deleted !" %(dbName) 
            conn.commit()
        else: 
            print "Database %s does not exist in current database ~" %(dbName)
    print "===========Prepare to clear Users ==============="
    for dbUser in userList:
        sqlQ='SELECT * from pg_user where usename =  \'%s\'' %(dbUser)
        print "Executing commands: ", sqlQ
        cur.execute(sqlQ)
        if bool(cur.rowcount):
            print "db user %s exists" %(dbUser)
            sqlD = "DROP user \"%s\";" %(dbUser)
            print "Executing commands: ", sqlD
            cur.execute(sqlD)
        else:
            print "User %s does not exist in current database ~" %(dbUser)
except (Exception,psycopg2.Error) as  error:
    print "Error when exec commands:", error
    conn.rollback()
finally:
    if(conn):
        cur.close()
        conn.close()
        print "Postgresql connnection is closed"
