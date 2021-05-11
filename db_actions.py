from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

class DBManagement:
    def get_table_names(self):
        return self.metadata.tables.keys()

    def get_table_columns(self, table_name):
        return self.engine.execute(f"SELECT * FROM {table_name} LIMIT 0").keys()

    def get_table(self, table_name):
        return self.engine.execute(f"SELECT * FROM {table_name}")
    
    def get_table_with_filter(self, table_name, filter:dict):
        print(filter)
        pass

    def delete_array(self, table_name, column, condition):
        return self.engine.execute(f"DELETE FROM {table_name} WHERE {table_name}.{column} IN {str(tuple(condition))}")

    def delete_single_value(self, table_name, column, condition):
        return self.engine.execute(
            f"DELETE FROM {table_name} WHERE {table_name}.{column}='{condition[0]}'")

    def delete_since_time(self, table_name, timestamp):
        print(f"DELETE FROM {table_name} WHERE timestamp >= '{timestamp}'")
        return self.engine.execute(
            f"DELETE FROM {table_name} WHERE {table_name}.timestamp>'{timestamp}'")

    def delete(self, tablename, column, condition):
        if condition is tuple or list:
            if len(condition) > 1:
                return self.delete_array(tablename, column, condition)
        return self.delete_single_value(tablename, column, condition)



class PostgersqlDBManagement(DBManagement):
    def __init__(self, username, password, url, dbname):
        self.engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{url}/{dbname}')
        self.metadata = MetaData()
        self.metadata.reflect(self.engine)
        self.Base = automap_base(metadata=self.metadata)
        self.Base.prepare()

class SQLiteDBManagement(DBManagement):
    def __init__(self, path_to_sqlite_db):
        self.engine = create_engine(f"sqlite+pysqlite:///{path_to_sqlite_db}")
        self.metadata = MetaData()
        self.metadata.reflect(self.engine)
        self.Base = automap_base(metadata=self.metadata)
        self.Base.prepare()
