from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import pandas as pd
from datetime import datetime

app = FastAPI()

@app.post("/convertir")
async def convertir(file: UploadFile = File(...)):
    df = pd.read_excel(file.file)
    fecha_actual = datetime.now().strftime("%Y%m%d")

    output_path = "/tmp/archivo_convertido.si1"

    columnas = [
        "InstructingParty", "SettlementParty", "SecuritiesAccount", "Instrument",
        "InstrumentIdentifierType", "CSDOfCounterparty", "SettlementCounterparty",
        "SecuritiesAccountOfCounterparty", "InstructionReference",
        "Instrument(MovementOfSecurities)", "Quantity", "QuantityType",
        "TransactionType", "SettlementMethod", "TradeDate",
        "IntendedSettlementDate", "PaymentType"
    ]

    filas = [";".join(columnas)]

    for i, row in df.iterrows():
        try:
            comitente = str(int(row[0])).strip()
            instrumento = row[1].split(')')[0].replace('(', '')
            disponible = float(row[2])
            instruction_reference = f"EA{datetime.now().strftime('%H%M%S')}{i:05d}"

            valores = [
                "81", "81", f"81/{comitente}", instrumento, "LOCAL_CODE", "CVSA", "309", f"9081/{comitente}",
                instruction_reference, "RECEIVE", str(disponible), "", "TRAD", "RTGS", fecha_actual, fecha_actual, "NOTHING"
            ]

            filas.append(";".join(valores))
        except:
            continue

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(filas))

    return FileResponse(output_path, filename="archivo_convertido.si1")
