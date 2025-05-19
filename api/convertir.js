const xlsx = require('xlsx');

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).send('Method Not Allowed');
  }

  try {
    const buffer = await req.arrayBuffer();
    const workbook = xlsx.read(buffer, { type: 'buffer' });
    const sheet = workbook.Sheets[workbook.SheetNames[0]];
    const data = xlsx.utils.sheet_to_json(sheet);

    const fecha = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    let resultado = '';

    for (const row of data) {
      try {
        const instrumento = row[Object.keys(row)[0]].match(/\\((.*?)\\)/)?.[1];
        const cantidad = row['Disponible'];
        const comitente = row['Comitente'];

        resultado += `:20:${fecha}\\n`;
        resultado += `:23G:NEWM\\n`;
        resultado += `:98A::TRAD//${fecha}\\n`;
        resultado += `:98A::SETT//${fecha}\\n`;
        resultado += `:35B:ISIN AR${instrumento}\\n`;
        resultado += `:94B::TRAD//XXXX/ARBA\\n`;
        resultado += `:16S:TRADDET\\n`;
        resultado += `:36B::SETT//FAMT/${cantidad}\\n`;
        resultado += `:97A::SAFE//81/${comitente}\\n`;
        resultado += `:97A::PSET//9081/${comitente}\\n`;
        resultado += `:16S:SETDET\\n`;
        resultado += `:16S:SETTRAN\\n`;
      } catch (e) {
        continue;
      }
    }

    res.setHeader('Content-Disposition', 'attachment; filename=archivo_convertido.si1');
    res.setHeader('Content-Type', 'application/octet-stream');
    res.send(resultado);

  } catch (error) {
    res.status(500).send('Error al procesar el archivo: ' + error.message);
  }
}
