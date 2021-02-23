import pyodbc 

server = '(localdb)\MSSQLLocalDB' 
database = 'geodezia' 
username = 'Rendszergazda' 
password = '' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
cursor = cnxn.cursor()
cursor.execute("SELECT id,name,content FROM dbo.files;")
count = 0

while True:
    row = cursor.fetchone()
    if (not row):break
    new_filename = 'files\\' + str(row[0]) + '_' + row[1]
    print('Exportálás...' + new_filename)
    count += 1
    
    with open(new_filename, 'wb') as f:
        f.write(row[2])
    
print('Exportálás befejeződött! (' + str(count) + ' elem)');    
