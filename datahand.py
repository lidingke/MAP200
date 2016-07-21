import sqlite3
import pdb

class DataHand(object):
    """docstring for DataHand"""
    def __init__(self, file = "script\\xlsdata\\data.db" ):
        super(DataHand, self).__init__()
        self.dbName = file

    def initTable(self,table):
        # localTime = str(int(localTime))
        # sqlTableName='TM'+localTime+'US'+username
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()
        try:
            #[('测试次数','通道数','波长','IL','ORL')]
            strEx='create table if not exists '+table+\
            ' ( No varchar(10), channel varchar(10), wave varchar(10),IL varchar(10), ORL varchar(10))'
            # print(strEx)
            cursor.execute(strEx)
        except Exception as e :
            raise e
        cursor.close()
        conn.commit()
        conn.close()
        # return sqlTableName

    def save2Sql(self,sqlTableName,data):

        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()
        try:
            strEx = 'insert into {} (No, channel, wave, IL, ORL) values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')'

            # change all the data into str
            strEx = strEx.format(sqlTableName,str(data[0]),data[1],
                data[2],data[3].decode('utf-8'),data[4].decode('utf-8'))
            # print(strEx)
            cursor.execute(strEx)
        except sqlite3.OperationalError as e :
            raise e
        except Exception as e:
            raise e
        cursor.close()
        conn.commit()
        conn.close()


    def getTableData(self,tableName):
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()
        try:
            strEx='select * from '+tableName
            cursor.execute(strEx)
        except sqlite3.OperationalError as e:
            print(e)

        data = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return data


    def getTableDataList(self,tableName,listName):
        conn = sqlite3.connect(self.dbName)
        cursor = conn.cursor()
        datalist = []
        for x in listName:
            try:
                strEx = 'select {} from '+tableName
                strEx = strEx.format(x)
                cursor.execute(strEx)
            except sqlite3.OperationalError as e:
                print(e)

            datalist.append(cursor.fetchall())
        cursor.close()
        conn.commit()
        conn.close()
        return datalist
