#!/usr/bin/python
import MySQLdb

db = MySQLdb.connect(host="db",       # your host
                     user="XXXXX",    # your username
                     passwd="XXXXX",  # your password
                     db="XXXXX",      # name of the db
                     port=XXX)        # name of the port

db2 = MySQLdb.connect(host="db",      # your host
                     user="XXXXX",    # your username
                     passwd="XXXXX",  # your password
                     db="XXXX",       # name of the db
                     port=XXXX)       # name of the port

cur = db.cursor()
cur2 = db2.cursor()

# Use the SQL
cur.execute("SELECT id, device_id FROM ports P JOIN ipallocations IP ON P.id = IP.port_id WHERE P.status = 'DOWN' ORDER BY device_id asc")

#add array id and device_id
device_id = cur.fetchall()
print  "*****************id*******************|*****************device_id***************"

#take only the second row
device_id_second_row = [x[1] for x in device_id]
device_ids = "'%s'" % "','".join(device_id_second_row)

# second query
cur2.execute("SELECT uuid, hostname, vm_state, created_at, deleted_at FROM instances WHERE deleted_at IS NOT NULL AND uuid IN (%s)" % device_ids)
result = cur2.fetchall()

# add dict and invert order to make device_id as key
dict_device = dict((y,x) for x,y in device_id)

# if exist the uuid in the device_id as key, print it
devices_deleted = []

for rows in result:
    if rows[0] in dict_device:
        devices_deleted.append(rows[0])
        print("({0}) {1}".format(dict_device[rows[0]], rows))

devices_down = [item for item in dict_device if item not in devices_deleted]
print "--------------------------------------------------------------------------------------------------------------------------------------------------"
print "---------------------------------------------------------DEVICES DOWN-----------------------------------------------------------------------------"
print devices_down

db.close()
db2.close()

print "--------------------------------------------------------------------------------------------------------------------------------------------------"
print "Total devices  ", len(dict_device)
print "Devices deleted", len(devices_deleted)
print "Devices down   ", len(devices_down)
print "--------------------------------------------------------------------------------------------------------------------------------------------------"

