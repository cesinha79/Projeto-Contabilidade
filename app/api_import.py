from fastapi import FastAPI, UploadFile, File
import pandas as pd
from .database import get_db_connection

app = FastAPI()

@app.post("/importar-contas-contabeis/")
async def importar_contas_contabeis(file: UploadFile = File(...)):
    data = pd.read_csv(file.file)
    conn = get_db_connection()
    data.to_sql('contas_contabeis', conn, if_exists='append', index=False)
    conn.close()
    return {"message": "Contas contábeis importadas com sucesso."}

@app.post("/importar-centros-custo/")
async def importar_centros_custo(file: UploadFile = File(...)):
    data = pd.read_csv(file.file)
    conn = get_db_connection()
    data.to_sql('centros_custo', conn, if_exists='append', index=False)
    conn.close()
    return {"message": "Centros de custo importados com sucesso."}

@app.post("/importar-lancamentos/")
async def importar_lancamentos(file: UploadFile = File(...)):
    data = pd.read_csv(file.file)
    conn = get_db_connection()
    data.to_sql('lancamentos', conn, if_exists='append', index=False)
    conn.close()
    return {"message": "Lançamentos contábeis importados com sucesso."}
