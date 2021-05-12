from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base


class DBManagement:
    def get_table_names(self):
        return self.metadata.tables.keys()

    def get_view_names(self):
        return [r for r, in self.engine.execute("select viewname from pg_catalog.pg_views where schemaname NOT IN ('pg_catalog', 'information_schema')order by schemaname, viewname;")]

    def get_table_columns(self, table_name):
        return self.engine.execute(f"SELECT * FROM {table_name} LIMIT 0").keys()

    def get_table_column_values(self, table_name, column_name):
        return [r for r, in self.engine.execute(f"SELECT {column_name} from {table_name} GROUP BY {column_name}")]

    def get_table(self, table_name, filter=None):
        filter = dict(filter)
        del filter["_"]
        if filter != {} :
            query_string = f"SELECT * FROM {table_name}"
            conditions = []
            print(filter)
            if "batchid" in filter:
                conditions.append(f"batch_inspectionid in (select batch_inspectionid from batchview where batchid = {filter['batchid']})")
            if "from_datetime" in filter:
                conditions.append(f"timestamp > '{filter['from_datetime'].replace('T', ' ')}'")
            if "to_datetime" in filter:
                conditions.append(f"timestamp < '{filter['to_datetime'].replace('T', ' ')}'")
            if len(conditions) > 0:
                query_string += " Where "
                query_string += " AND ".join(conditions)
            return self.engine.execute(query_string)
        if filter == {}:
            return self.engine.execute(f"SELECT * FROM {table_name}")

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
        self.engine = create_engine(
            f'postgresql+psycopg2://{username}:{password}@{url}/{dbname}')
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
