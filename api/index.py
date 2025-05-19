
from flask import Flask, request, send_file, make_response
import pandas as pd
import datetime
import io

app = Flask(__name__)

@app.route('/api/convertir', methods=['POST'])
def convertir():
    if 'file' not in request.files:
        return "No se envió ningún archivo", 400

    file = request.files['file']
    try:
        df = pd.read_excel(file, dtype=str)
    except Exception as e:
        return f"No se pudo leer el archivo: {e}", 400

    fecha = datetime.datetime.now().strftime('%Y%m%d')
    contenido = ""

    for _, row in df.iterrows():
        try:
            instrumento = row[0].split("(")[-1].strip(")")
            cantidad = row["Disponible"]
            comitente = str(row["Comitente"])

            contenido += (
                f":20:{fecha}\n"
                f":23G:NEWM\n"
                f":98A::TRAD//{fecha}\n"
                f":98A::SETT//{fecha}\n"
                f":35B:ISIN AR{instrumento}\n"
                f":94B::TRAD//XXXX/ARBA\n"
                f":16S:TRADDET\n"
                f":36B::SETT//FAMT/{cantidad}\n"
                f":97A::SAFE//81/{comitente}\n"
                f":97A::PSET//9081/{comitente}\n"
                f":16S:SETDET\n"
                f":16S:SETTRAN\n"
            )
        except:
            continue

    output = io.BytesIO()
    output.write(contenido.encode("utf-8"))
    output.seek(0)

    response = make_response(send_file(output, as_attachment=True, download_name="archivo_convertido.si1"))
    response.headers["Content-Type"] = "application/octet-stream"
    return response
