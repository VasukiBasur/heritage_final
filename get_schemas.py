import mysql.connector, os, dotenv
dotenv.load_dotenv()
db=mysql.connector.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), database=os.getenv('DB_NAME'))
cursor=db.cursor()
tables=['artisans','raw_materials','suppliers','product_catalog']
for t in tables:
    cursor.execute(f'DESCRIBE {t}')
    print(f'--- {t} ---')
    for r in cursor.fetchall():
        print(str(repr(r)).encode('ascii', 'ignore').decode('ascii'))
