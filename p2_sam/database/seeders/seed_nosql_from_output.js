"use strict";

const fs = require("fs");
const path = require("path");
const mongoose = require("mongoose");

const connectMongoDB = require("../nosql/connections");
const FinancialAudit = require("../nosql/schemas/financial_log");
const InteractionLog = require("../nosql/schemas/interaction_log");
const IotTelemetry = require("../nosql/schemas/iot_telemetry");
const Notification = require("../nosql/schemas/notification");
const Voucher = require("../nosql/schemas/vouchers");

const OUTPUT_DIR = process.env.OUTPUT_DIR
 ? path.resolve(process.env.OUTPUT_DIR)
 : path.resolve(__dirname, "../../../output");

const SHOULD_CLEAR = process.env.SEED_CLEAR !== "false";

function readOutput(fileName) {
 const filePath = path.join(OUTPUT_DIR, fileName);
 return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function normalizeFinancialLog(record) {
 return {
  transacao_sql_id: record.transacao_sql_id,
  metodo: record.metodo,
  data_hora: record.data_hora ?? record.data,
  status_gateway: record.status_gateway,
  gateway_response: record.gateway_response,
  gateway: record.gateway,
  telemovel_hash: record.telemovel_hash,
  codigo_aprovacao: record.codigo_aprovacao,
  id_pedido_sibs: record.id_pedido_sibs,
  ip_dispositivo: record.ip_dispositivo,
  tentativas: record.tentativas,
  motivo_erro: record.motivo_erro,
 };
}

function normalizeInteractionLog(record) {
 return {
  sessao_id: record.sessao_id,
  painel_id: record.painel_id,
  inicio_sessao: record.inicio_sessao,
  duracao_segundos: record.duracao_segundos ?? record.duracao_interacao,
  fluxo_navegacao: record.fluxo_navegacao,
  concluiu_doacao: record.concluiu_doacao,
  passo_abandono: record.passo_abandono,
  idioma: record.idioma,
 };
}

function normalizeIotTelemetry(record) {
 return {
  timestamp: record.timestamp,
  evento: record.evento,
  dispositivo_id: record.dispositivo_id ?? record.locker_id,
  tipo: record.tipo,
  localizacao: {
   geo_latitude: record.geo_latitude,
   geo_longitude: record.geo_longitude,
  },
  telemetria: {
   bateria_voltagem: record.bateria_voltagem ?? record.bateria_estado,
   cpu_temp: record.cpu_temp ?? record.cpu_temperatura,
   sinal_dbm: record.sinal_dbm ?? record.dmb_sinal,
   aviso: record.aviso,
  },
  status: record.status,
  versao: record.versao,
 };
}

function normalizeVoucher(record) {
 return {
  montante: Number(record.montante),
  data_emissao: record.data_emissao,
  estado: record.estado,
  validade: record.validade,
  entidade_disponivel_levantamento:
   record.entidade_disponivel_levantamento ?? record.entidades_disp,
  negocio_nif_nipc: record.negocio_nif_nipc,
  data_uso: record.data_uso,
 };
}

const seedPlan = [
 {
  model: FinancialAudit,
  file: "nosql_financial_log.json",
  transform: normalizeFinancialLog,
 },
 {
  model: InteractionLog,
  file: "nosql_interaction_log.json",
  transform: normalizeInteractionLog,
 },
 {
  model: IotTelemetry,
  file: "nosql_locker_telemetry.json",
  transform: normalizeIotTelemetry,
 },
 {
  model: Notification,
  file: "nosql_notification.json",
 },
 {
  model: Voucher,
  file: "nosql_vouchers.json",
  transform: normalizeVoucher,
 },
];

async function seedCollection({ model, file, transform }) {
 const records = readOutput(file).map((record) =>
  transform ? transform(record) : record,
 );

 if (SHOULD_CLEAR) {
  try {
   await model.collection.drop();
  } catch (error) {
   if (error.codeName !== "NamespaceNotFound") {
    throw error;
   }
  }
 }

 if (!records.length) {
  console.log(`[NoSQL] ${model.collection.name}: sem documentos`);
  return;
 }

 await model.collection.insertMany(records, { ordered: false });
 console.log(
  `[NoSQL] ${model.collection.name}: ${records.length} documentos inseridos`,
 );
}

async function main() {
 await connectMongoDB();

 try {
  for (const step of seedPlan) {
   await seedCollection(step);
  }
 } finally {
  await mongoose.disconnect();
 }
}

main().catch((error) => {
 console.error("[NoSQL] erro ao importar dados:", error);
 process.exit(1);
});
