# dependencies
import pandas as pd
import numpy as np
import sqlalchemy
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, join, outerjoin
from sqlalchemy import Table, MetaData, func

class CorgiData():

    def __init__(self):
        self.connect_string = os.environ.get('DATABASE_URL', '') or "sqlite:///corgies.db"
        self.engine = create_engine(self.connect_string)


        self.Base = automap_base()
        self.Base.prepare(self.engine, reflect=True)

        self.Pets = self.Base.classes['pets']
        self.meta = MetaData()
        self.PetTraining = Table('pet_training', self.meta, autoload_with=self.engine)


    def display_db_info(self):
        inspector = inspect(self.engine)
        tables = self.inspector.get_table_names()
        for table in self.tables:
            print("\n")
            print('-' * 12)
            print(f"table '{table}' has the following columns:")
            print('-' * 12)
            for column in self.inspector.get_columns(table):
                print(f"name: {column['name']}   column type: {column['type']}") 

    
    
    #ORM approach
    def get_pet_data(self, name=""):
        session = Session(self.engine)
        if name == "":
            results = session.query(self.Pets)
        else:
            results = session.query(self.Pets).filter(self.Pets.name == name)
            
        pet_df = pd.read_sql(results.statement, session.connection())
        session.close()  
        return pet_df.to_dict(orient="records")     

    

    # sql engine approach
    def get_pet_training_data(self, name=""):
        if name == "":
            sql = "select * from pet_training"
        else:
            cur_name = name.lower()
            sql = f"select * from pet_training where lower(name) = '{cur_name}'"  

        conn = self.engine.connect()
        training_df = pd.read_sql(sql, conn) 
        conn.close()
        return training_df.to_dict(orient='records')  

    # use ORM to dynamically create query from query parms
    def get_pet_training_orm(self, parm_dict):
        session = Session(self.engine)
        table_columns = [c.name for c in self.PetTraining.columns]

        results = session.query(self.PetTraining)
        for k, v in parm_dict.items():
            if k == 'name':
                results = results.filter_by(name = v)
            elif k == 'grade':
                v = v.upper()
                results = results.filter_by(grade = v) 
            elif k == 'task':
                results = results.filter_by(task = v )    

        pet_df = pd.read_sql(results.statement, session.connection())
        session.close()  
        return pet_df.to_dict(orient="records") 
           

if __name__ == '__main__':
    corgies = CorgiData()
    print(corgies.get_pet_data())
    print('*' * 15, "Patterson Only")
    print(corgies.get_pet_data("Patterson"))
    print('*' * 15)
    print(corgies.get_pet_training_data())
    print('*' * 15, "Patterson Only")
    print(corgies.get_pet_training_data('PATTERSON'))


        