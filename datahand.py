import sqlite3


class DataHand(object):
    """docstring for DataHand"""
    def __init__(self, file = "data.db" ):
        super(DataHand, self).__init__()
        self.dbName = file

    def initTable(self,table):
        # localTime = str(int(localTime))
        # sqlTableName='TM'+localTime+'US'+username
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        try:
            strEx='create table if not exists '+table+\
            ' ( power varchar(10), data varchar(10))'
            cursor.execute(strEx)
        except Exception as e:
            raise e
        cursor.close()
        conn.commit()
        conn.close()
        # return sqlTableName

    def saveData(self,table,):
        pass
