
from faker import Faker
from datetime import datetime, timedelta, time
import psycopg2
import time
import dotenv
import os
import schedule
import json

# utilzando o dotenv para proteger as variáveis de ambiente
# carrega para a memória os valores 
path_env = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv(path_env)

fake = Faker()


def generateData() -> dict:
    lat, lng, region, country, timezone = fake.location_on_land()
    create_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    profile = fake.profile()
    return dict(
        {
            "created_at": create_date,
            "updated_at": create_date,
            "customer_id": fake.uuid4(),
            "name": profile.get("name"),
            "gender": profile.get("sex"),
            "birthday": profile.get("birthdate"),
            "blood_group": profile.get("blood_group"),
            "email": profile.get("mail"),
            "phone_number": fake.phone_number(),
            "address": profile.get("address"),
            "region": region,
            "country": country,
            "lat": lat,
            "lng": lng,
        }
    )


def createTable() -> str:
    return """
    create table if not exists customers(
        created_at TIMESTAMP NOT NULL ,
        updated_at TIMESTAMP,
        customer_id UUID PRIMARY KEY,
        name VARCHAR (100),
        gender CHAR (1),
        birthday DATE,
        blood_group VARCHAR(3),
        email VARCHAR (100),
        address VARCHAR (200),
        phone_number VARCHAR (30),
        region VARCHAR (100),
        country VARCHAR (100),
        lat FLOAT,
        lng FLOAT
    )
"""


def connDB() -> psycopg2.connect:

    user = os.getenv(key="user")
    password = os.getenv(key="key")
    host = os.getenv(key="dns")
    port = "5432"
    dbname = "btwoc"

    conn = psycopg2.connect(
       dbname= dbname, user=user, password=password, host=host, port=port 
    )
    # inserir log
    conn.set_session(autocommit=True)
    return conn 
         
    # except psycopg2.Error as e:
    #     print(e)
    
   
def ddlSQL() -> None:

    # with connDB() as conect:
    conect = connDB()
    # conect.set_session(autocommit=True)
    print('sucess conn')
    cursor = conect.cursor()
    ddl = createTable()
    cursor.execute(ddl)
    cursor.close()
    
    # inserir log
    

def insertSQL() -> str:
    return """
    insert into customers values(
        '{created_at}',
        '{updated_at}',
        '{customer_id}',
        '{name}',
        '{gender}',
        '{birthday}',
        '{blood_group}',
        '{email}',
        '{address}',
        '{phone_number}',
        '{region}',
        '{country}',
        '{lat}',
        '{lng}'
        )
        """.format(
        **generateData()
    )

ddlSQL()

while True:
    
    query = insertSQL()
    # with connDB() as conn:
    conn = connDB()
    cursor = conn.cursor()
    # schedule.every(1).hours.until(timedelta(minutes=10)).do(cursor.execute(query))
    cursor.execute(query)
    # log
    print(query)
    time.sleep(0.5)



