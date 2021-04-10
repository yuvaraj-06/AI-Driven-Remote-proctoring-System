from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from os.path import dirname, join
cloud_config= {
        'secure_connect_bundle': join(dirname(__file__), "secure-connect-database.zip")}
auth_provider = PlainTextAuthProvider('Datauser', 'database@1')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

row = session.execute("select release_version from system.local").one()
if row:
    print(row[0])
else:
    print("An error occurred.")

############


session.set_keyspace('data')
#futures = []
#user="yuvaraj"

#query = "CREATE TABLE teacher ( id text, psw text,trans text,PRIMARY KEY(id));"
#a=session.execute_async(query)
#a.result()

#print("done") 

#insert_statement = session.prepare("INSERT INTO teacher (id,psw,trans) VALUES (?,?,?)")
#session.execute(insert_statement, ["Prof A","1234","todau is calss"]) 
futures = []
query = "SELECT * FROM teacher"
ids_to_fetch=[1]
for user_id in ids_to_fetch:
    futures.append(session.execute_async(query))
for i in futures:
    rows = i.result()
    a=rows[0]
#a=a.strip('][').split(',') 
print(a)  