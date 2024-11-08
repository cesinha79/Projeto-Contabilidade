from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from .database import get_db_connection
import sqlite3

router = APIRouter()

@router.post("/importar-contas-contabeis/")
async def importar_contas_contabeis(file: UploadFile = File(...)):
    try:
        data = pd.read_csv(file.file)
        conn = get_db_connection()
        data.to_sql('contas_contabeis', conn, if_exists='append', index=False)
        conn.close()
        return {"message": "Contas contábeis importadas com sucesso."}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Erro de integridade: possivelmente IDs duplicados.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/importar-centros-custo/")
async def importar_centros_custo(file: UploadFile = File(...)):
    try:
        data = pd.read_csv(file.file)
        conn = get_db_connection()
        data.to_sql('centros_custo', conn, if_exists='append', index=False)
        conn.close()
        return {"message": "Centros de custo importados com sucesso."}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Erro de integridade: possivelmente IDs duplicados.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/importar-lancamentos/")
async def importar_lancamentos(file: UploadFile = File(...)):
    try:
        data = pd.read_csv(file.file)
        conn = get_db_connection()
        data.to_sql('lancamentos', conn, if_exists='append', index=False)
        conn.close()
        return {"message": "Lançamentos contábeis importados com sucesso."}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Erro de integridade: possivelmente IDs duplicados.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
