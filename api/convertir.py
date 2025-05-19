
import pandas as pd
import datetime
import base64

def handler(request):
    try:
        if request.method != "POST":
            return {
                "statusCode": 405,
                "headers": { "Content-Type": "text/plain" },
                "body": "Método no permitido"
            }

        file = request.files.get("file")
        if not file:
            return {
                "statusCode": 400,
                "headers": { "Content-Type": "text/plain" },
                "body": "No se proporcionó archivo"
            }

        df = pd.read_excel(file.file, dtype=str)

        hoy = datetime.datetime.now().strftime("%Y%m%d")
        resultado = ""

        for _, row in df.iterrows():
            try:
                instrumento = row[0].split("(")[-1].strip(")")
                cantidad = row["Disponible"]
                comitente = str(row["Comitente"])

                resultado += (
                    f":20:{hoy}\n"
                    f":23G:NEWM\n"
                    f":98A::TRAD//{hoy}\n"
                    f":98A::SETT//{hoy}\n"
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

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/octet-stream",
                "Content-Disposition": "attachment; filename=archivo_convertido.si1"
            },
            "body": base64.b64encode(resultado.encode()).decode(),
            "isBase64Encoded": True
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": { "Content-Type": "text/plain" },
            "body": f"Error interno: {str(e)}"
        }
