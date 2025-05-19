
import pandas as pd
import io
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

        form_data = request.files
        file = form_data.get("file")
        if not file:
            return {
                "statusCode": 400,
                "headers": { "Content-Type": "text/plain" },
                "body": "Archivo no proporcionado"
            }

        # Leer Excel (.xls o .xlsx)
        df = pd.read_excel(file.file, dtype=str)

        # Obtener fecha actual en formato YYYYMMDD
        fecha_actual = datetime.datetime.now().strftime("%Y%m%d")

        contenido = ""
        for _, row in df.iterrows():
            try:
                instrumento = row[0].split("(")[-1].strip(")")
                cantidad = row["Disponible"]
                comitente = str(row["Comitente"])

                contenido += (
                    f":20:{fecha_actual}\n"
                    f":23G:NEWM\n"
                    f":98A::TRAD//{fecha_actual}\n"
                    f":98A::SETT//{fecha_actual}\n"
                    f":35B:ISIN AR{instrumento}\n"
                    f":94B::TRAD//XXXX/ARBA\n"
                    f":16S:TRADDET\n"
                    f":36B::SETT//FAMT/{cantidad}\n"
                    f":97A::SAFE//81/{comitente}\n"
                    f":97A::PSET//9081/{comitente}\n"
                    f":16S:SETDET\n"
                    f":16S:SETTRAN\n"
                )
            except Exception:
                continue

        # Convertir a bytes
        output_bytes = contenido.encode("utf-8")

        # Devolver como archivo para descargar
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/octet-stream",
                "Content-Disposition": "attachment; filename=archivo_convertido.si1"
            },
            "body": base64.b64encode(output_bytes).decode("utf-8"),
            "isBase64Encoded": True
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": { "Content-Type": "text/plain" },
            "body": f"Error interno: {str(e)}"
        }
