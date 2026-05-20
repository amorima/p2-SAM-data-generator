"use strict";

const fs = require("fs");
const path = require("path");
const { sequelize } = require("../models");

const OUTPUT_DIR = process.env.OUTPUT_DIR
 ? path.resolve(process.env.OUTPUT_DIR)
 : path.resolve(__dirname, "../../../output");

const SHOULD_CLEAR = process.env.SEED_CLEAR !== "false";

function readOutput(fileName) {
 const filePath = path.join(OUTPUT_DIR, fileName);
 return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function onlyFields(record, fields) {
 return fields.reduce((result, field) => {
  if (Object.prototype.hasOwnProperty.call(record, field)) {
   result[field] = record[field];
  }

  return result;
 }, {});
}

function normalizeCidadao(record) {
 return {
  ...record,
  blocked: record.blocked ?? 0,
  role: record.role ?? "citizen",
 };
}

const seedPlan = [
 {
  table: "localidade",
  file: "localidade.json",
  fields: [
   "codigo_postal",
   "concelho",
   "distrito",
   "freguesia",
   "pais",
   "rua",
   "n_porta",
  ],
 },
 {
  table: "entidade",
  file: "entidade.json",
  fields: [
   "nif_nipc",
   "email_login",
   "password",
   "nome_entidade",
   "iban",
   "codigo_postal",
   "profile_pic",
   "role",
  ],
 },
 { table: "mecena", file: "mecena.json", fields: ["nif_nipc"] },
 {
  table: "negocio",
  file: "negocio.json",
  fields: [
   "nif_nipc",
   "geo_latitude",
   "geo_longitude",
   "url_certidao_permanente",
   "inicio_atividade",
  ],
 },
 {
  table: "instituicao",
  file: "instituicao.json",
  fields: [
   "nif_nipc",
   "geo_latitude",
   "geo_longitude",
   "url_comprovativo_estatuto",
  ],
 },
 {
  table: "localidade_entidade",
  file: "localidade_entidade.json",
  fields: ["entidade_nif_nipc", "localidade_codigo_postal"],
 },
 {
  table: "contacto",
  file: "contacto.json",
  fields: ["contacto", "entidade_nif_nipc", "nome_contacto", "descricao"],
 },
 {
  table: "cidadao",
  file: "cidadao.json",
  transform: normalizeCidadao,
  fields: ["nome", "contacto", "rgpd", "blocked", "role", "reason"],
 },
 {
  table: "doacao",
  file: "doacao.json",
  fields: [
   "id_doacao",
   "mecena_nif_nipc",
   "data",
   "valor_transacao",
   "tipo_donativo",
   "anonimo",
   "url_comprovativo",
   "estado",
  ],
 },
 {
  table: "painel",
  file: "painel_digital.json",
  fields: [
   "id_dispositivo",
   "token_api",
   "geo_latitude",
   "geo_longitude",
   "raio_alcance",
  ],
 },
 {
  table: "locker_inteligente",
  file: "locker.json",
  fields: [
   "id_locker",
   "estado",
   "codigo_mestre",
   "geo_latitude",
   "geo_longitude",
  ],
 },
 {
  table: "bens_e_servicos",
  file: "bens_servicos.json",
  fields: ["tipo_bem_servico", "tipo_bem"],
 },
 {
  table: "pedido",
  file: "pedido.json",
  fields: ["id_pedido", "nif_nipc", "estado"],
 },
 {
  table: "pedido_bens_e_servicos",
  file: "pedido_bens_servicos.json",
  fields: ["id_pedido", "tipo_bem_servico", "publico"],
 },
 {
  table: "bens_e_servicos_negocio",
  file: "bens_servicos_negocio.json",
  fields: [
   "negocio_nif_nipc",
   "tipo_bem_servico",
   "descricao",
   "valor_total",
   "desconto",
  ],
 },
 {
  table: "leads",
  file: "lead.json",
  fields: [
   "id_lead",
   "data",
   "id_painel",
   "nome_cidadao",
   "contacto_cidadao",
   "id_pedido",
   "item_pedido",
   "estado",
   "pin_entrega",
   "id_locker",
  ],
 },
];

async function clearTables(queryInterface) {
 await sequelize.query("SET FOREIGN_KEY_CHECKS = 0");

 for (const { table } of [...seedPlan].reverse()) {
  await queryInterface.bulkDelete(table, null, {});
 }

 await sequelize.query("SET FOREIGN_KEY_CHECKS = 1");
}

async function seedTable(queryInterface, step) {
 const source = readOutput(step.file);
 const records = source.map((record) => {
  const normalized = step.transform ? step.transform(record) : record;
  return onlyFields(normalized, step.fields);
 });

 if (!records.length) {
  console.log(`[SQL] ${step.table}: sem registos`);
  return;
 }

 await queryInterface.bulkInsert(step.table, records, {});
 console.log(`[SQL] ${step.table}: ${records.length} registos inseridos`);
}

async function main() {
 const queryInterface = sequelize.getQueryInterface();

 try {
  await sequelize.authenticate();

  if (SHOULD_CLEAR) {
   await clearTables(queryInterface);
  }

  for (const step of seedPlan) {
   await seedTable(queryInterface, step);
  }
 } finally {
  await sequelize.close();
 }
}

main().catch((error) => {
 console.error("[SQL] erro ao importar dados:", error);
 process.exit(1);
});
