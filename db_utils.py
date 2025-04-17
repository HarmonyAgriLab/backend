import pymysql

from get_config import *

mysql_config_list = get_mysql_config()

host = mysql_config_list['host']
username = mysql_config_list['username']
password = mysql_config_list['password']
database = mysql_config_list['database']

def connect(host, user_name, password, database):
    try:
        db = pymysql.connect(host=host, user=username, password=password, database=database)
        cursor = db.cursor()
        return db, cursor
    except Exception as e:
        print(f'in connect catch err:{e}')

def insert(db, cursor, table_name, datas_dict):
    try:
        columns = ', '.join(datas_dict.keys())
        placeholders = ', '.join(['%s'] * len(datas_dict))
        values = list(datas_dict.values())
        schema = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        cursor.execute(schema, values)
        db.commit()
        print(f'insert success,datas:{datas_dict}')    
    except Exception as e:
        print(f'in insert,catch err:{e}')

def delete(db, cursor, table_name, id):
    try:
        schema = f'DELETE FROM {table_name} WHERE id = (%s)'
        cursor.execute(schema,(id,))
        db.commit()
        print(f'delete success,id:{id}')
    except Exception as e:
        print(f'in delete,catch err:{e}')

def deleteAll(db, cursor):
    try:
        pass
    except Exception as e:
        print(f'in deleteAll,catch err:{e}')

def update(db, cursor, msg, name):
    try:
        pass
    except Exception as e:
        print(f'in update,catch err:{e}')
        
def queryById(cursor, table_name, id):
    returnVal = []
    try:
        schema = f'SELECT * FROM {table_name} WHERE id = (%s)'
        cursor.execute(schema,(id,))
        datas = cursor.fetchall()
        if table_name == 'air':
            for data in datas:
                returnVal = [data[1], data[2], data[3], data[4]]
        elif table_name == 'soil':
            for data in datas:
                returnVal = [data[2], data[1], data[3], data[4], data[5], data[6], data[7],data[8],data[9]]
        print(f'queryById success,data:{returnVal}')
        return returnVal
    except Exception as e:
        print(f'in query,catch err:{e}')
        return returnVal

def queryAll(cursor, table_name):
    returnVals = []
    try:
        schema = f'SELECT * FROM {table_name}'
        cursor.execute(schema)
        datas = cursor.fetchall()
        if table_name == 'air':
            for data in datas:
                returnVal = [data[1], data[2], data[3], data[4]]
                returnVals.append(returnVal)
        elif table_name == 'soil':
            for data in datas:
                returnVal = [data[2], data[1], data[3], data[4], data[5], data[6], data[7],data[8],data[9]]
                returnVals.append(returnVal)
        print(f'queryAll success,datas:{returnVals}')
        return returnVals
    except Exception as e:
        print(f'in query,catch err:{e}')
        return returnVals

if __name__=='__main__':
    db, cursor = connect(host, username, password, database)
    if cursor:
        # insertVals = {
        #     'air_temp': 19.2,
        #     'air_humid': 15,
        #     'device_mac': 'AA-BB-CC-DD-EE-FF'
        # }
        # insert(db, cursor, 'air', insertVals)
        queryAll(cursor, 'air')
