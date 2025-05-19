import pandas as pd
from datetime import datetime
import tempfile
import os

def handler(request, response):
    # Parse the uploaded file from the request
    form = request.files
    if "file" not in form:
        response.status_code = 400
        response.body = "No file uploaded"
        return

    file = form["file"]
    df = pd.read_excel(file.file)
    fecha_actual = datetime.now().strftime("%Y%m%d")

    # Use a temp file for output
    with tempfile.NamedTemporaryFile(delete=False, suffix=".si1") as tmp:
        output_path = tmp.name

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

    # Return the file as a response
    response.headers["Content-Type"] = "application/octet-stream"
    response.headers["Content-Disposition"] = "attachment; filename=archivo_convertido.si1"
    with open(output_path, "rb") as f:
        response.body = f.read()

    os.remove(output_path)