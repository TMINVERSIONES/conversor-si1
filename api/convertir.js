
import formidable from 'formidable';
import fs from 'fs';
import xlsx from 'xlsx';

export const config = {
  api: {
    bodyParser: false
  }
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).send('Method Not Allowed');
  }

  const form = formidable({ multiples: false });

  form.parse(req, async (err, fields, files) => {
    if (err || !files.file) {
      return res.status(400).send('Error al procesar el archivo');
    }

    try {
      const filePath = files.file[0].filepath;
      const workbook = xlsx.readFile(filePath);
      const sheet = workbook.Sheets[workbook.SheetNames[0]];
      const data = xlsx.utils.sheet_to_json(sheet, { defval: "" });

      const fecha = new Date().toISOString().slice(0, 10).replace(/-/g, '');
      let resultado = "InstructingParty;SettlementParty;SecuritiesAccount;Instrument;InstrumentIdentifierType;CSDOfCounterparty;SettlementCounterparty;SecuritiesAccountOfCounterparty;InstructionReference;Instrument(MovementOfSecurities);Quantity;QuantityType;TransactionType;SettlementMethod;TradeDate;IntendedSettlementDate;PaymentType\n";

      let contador = 0;

      for (const row of data) {
        try {
          const instrumento = String(row["Instrumento"] || "").match(/\((.*?)\)/)?.[1];
          const cantidad = row["Disponible"];
          const comitente = row["Comitente"];

          if (!instrumento || !cantidad || !comitente) continue;

          const referencia = "EA575105710000" + String(contador).padStart(2, "0");

          const linea = [
            "81", "81", `81/${comitente}`,
            instrumento, "LOCAL_CODE", "CVSA", "309", `9081/${comitente}`,
            referencia, "RECEIVE", cantidad, "", "TRAD", "RTGS", fecha, fecha, "NOTHING"
          ].join(";");

          resultado += linea + "\n";
          contador++;

        } catch {
          continue;
        }
      }

      res.setHeader('Content-Disposition', 'attachment; filename=archivo_convertido.si1');
      res.setHeader('Content-Type', 'application/octet-stream');
      res.send(resultado);

    } catch (error) {
      res.status(500).send('Error interno: ' + error.message);
    }
  });
}
