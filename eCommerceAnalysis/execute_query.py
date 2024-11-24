
#executar comandos sql funciona diferente dependendo da versão do sql alchemy aparentemente
#why did they change this
#https://stackoverflow.com/questions/75316741/attributeerror-engine-object-has-no-attribute-execute-when-trying-to-run-sq

import sqlalchemy
from sqlalchemy import text
#precisa de 2 imports da mesma coisa wtf

def execute_sql(engine, sql, params = {}):
    if (sqlalchemy.__version__).startswith('1.4.'):
        return engine.execute(sql, params) 
    else: # 2.0.0
        with engine.connect() as conn: 
            result = conn.execute(text(sql), params)
            conn.commit()
            return result