import sqlite3

db_name="database.db"

#function to create db connection
def create_connection(db_file):
    try:
        conn=sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
        return None

# function to run sql query
def run_query(sql_query,args=[]):
    conn=create_connection(db_name)
    cur=conn.cursor()
    if sql_query.lower().startswith("select"):
        cur.execute(sql_query,args)
        return cur.fetchall()
    else:
        cur.execute(sql_query,args)
    try:
        conn.commit()
    except Exception as e:
        print(e)

#for creating table
def create_table():
    sql_query=""" create table if not exists weather_report(
        id integer primary key,
        location text,
        description text,
        temp text,
        time TIMESTAMP

    );
    """
    run_query(sql_query)

#to insert new entries into table
def insert_into_weather(location,description,temp,time):
    sql_query="""insert into weather_report(location,description,temp,time) values (?,?,?,?)
    """
    run_query(sql_query,[location,description,temp,time])
    print("\n new values added into table \n")

#to get all values based on location 
def get_value_from_DB(location):
    sql_query="""select description,temp,time from weather_report where location = ? """
    print("\n extracting values from table \n")
    return run_query(sql_query,[location])

#to print all values from table
def print_val():
    sql_query="""select * from weather_report
    """
    return run_query(sql_query)
#to delete old value
def delete_record(location):
    sql_query="""DELETE FROM weather_report WHERE location = ? """
    run_query(sql_query,[location])
    print("\nold value deleted\n")


#for db connection
create_connection(db_name)
print("\nDB connected ! \n")
create_table()
