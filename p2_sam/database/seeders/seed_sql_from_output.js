"use strict";

const fs = require("fs");
const path = require("path");
const bcrypt = require("bcryptjs");
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

function dedupEmailLogin(records) {
 const seen = new Map();
 return records.map((r) => {
  const base = r.email_login;
  if (!seen.has(base)) {
   seen.set(base, 1);
   return r;
  }
  const count = seen.get(base) + 1;
  seen.set(base, count);
  const [local, domain] = base.split("@");
  return { ...r, email_login: `${local}${count}@${domain}`.slice(0, 45) };
 });
}

function normalizeCidadao(record) {
 return {
  ...record,
  blocked: record.blocked ?? 0,
 };
}

function dedupCidadaoByNome(records) {
 const seen = new Set();
 return records.filter((r) => {
  if (seen.has(r.nome)) return false;
  seen.add(r.nome);
  return true;
 });
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
  transform: (r) => ({ ...r, iban: r.iban?.slice(0, 23), nome_entidade: r.nome_entidade?.slice(0, 45) }),
  postProcess: dedupEmailLogin,
  fields: [
   "nif_nipc",
   "email_login",
   "password",
   "nome_entidade",
   "iban",
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
  postProcess: dedupCidadaoByNome,
  fields: ["nome", "contacto", "rgpd", "blocked", "reason"],
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
  fields: ["id_pedido", "nif_nipc", "estado", "data"],
 },
 {
  table: "pedido_bens_e_servicos",
  file: "pedido_bens_servicos.json",
  fields: ["id_pedido", "tipo_bem_servico"],
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
 { table: "leads" }, // cleared here; seeded separately after pedido_bens_e_servicos query
];

async function clearTables(queryInterface) {
 await sequelize.query("SET FOREIGN_KEY_CHECKS = 0");

 for (const { table } of [...seedPlan].reverse()) {
  await queryInterface.bulkDelete(table, null, {});
 }

 await sequelize.query("SET FOREIGN_KEY_CHECKS = 1");
}

const validCidadaoContactos = new Set();

async function seedTable(queryInterface, step) {
 const source = readOutput(step.file);
 let records = source.map((record) => {
  const normalized = step.transform ? step.transform(record) : record;
  return onlyFields(normalized, step.fields);
 });

 if (step.postProcess) {
  records = step.postProcess(records);
 }

 if (step.table === "cidadao") {
  for (const r of records) {
   if (r.contacto) validCidadaoContactos.add(r.contacto);
  }
 }

 if (!records.length) {
  console.log(`[SQL] ${step.table}: sem registos`);
  return;
 }

 await queryInterface.bulkInsert(step.table, records, {});
 console.log(`[SQL] ${step.table}: ${records.length} registos inseridos`);
}

async function seedLeads(queryInterface) {
 const source = readOutput("lead.json");
 const allRecords = source.map((r) =>
  onlyFields(r, [
   "id_lead", "data", "id_painel", "nome_cidadao", "contacto_cidadao",
   "id_pedido", "item_pedido", "estado", "pin_entrega", "id_locker",
  ])
 );

 const records = validCidadaoContactos.size
  ? allRecords.filter((r) => validCidadaoContactos.has(r.contacto_cidadao))
  : allRecords;

 const skipped = allRecords.length - records.length;
 if (skipped > 0) {
  console.log(`[SQL] leads: ${skipped} registos ignorados (cidadão inexistente após dedup)`);
 }

 if (!records.length) {
  console.log("[SQL] leads: sem registos");
  return;
 }

 await queryInterface.bulkInsert("leads", records, {});
 console.log(`[SQL] leads: ${records.length} registos inseridos`);
}

async function fixLeadsIdItem() {
 try {
  await sequelize.query(`
   UPDATE leads l
   INNER JOIN pedido_bens_e_servicos pbs
    ON pbs.id_pedido = l.id_pedido AND pbs.tipo_bem_servico = l.item_pedido
   SET l.id_item = pbs.id_item
   WHERE l.id_item IS NULL
  `);
  console.log("[SQL] fixLeadsIdItem: leads.id_item populated from pedido_bens_e_servicos");
 } catch (e) {
  console.warn(`[SQL] fixLeadsIdItem: ${e.message}`);
 }
}

async function fixAutoIncrements() {
 const fixes = [
  "ALTER TABLE `doacao` MODIFY `id_doacao` INT NOT NULL AUTO_INCREMENT",
  "ALTER TABLE `leads` MODIFY `id_lead` INT NOT NULL AUTO_INCREMENT",
  "ALTER TABLE `pedido` MODIFY `id_pedido` INT NOT NULL AUTO_INCREMENT",
 ];
 for (const sql of fixes) {
  try {
   await sequelize.query(sql);
  } catch (e) {
   console.warn(`[SQL] fixAutoIncrements: ${e.message}`);
  }
 }
 console.log("[SQL] fixAutoIncrements: colunas AUTO_INCREMENT verificadas");
}

async function seedAdmin(queryInterface) {
 const adminNif = process.env.ADMIN_NIF;
 const adminEmail = process.env.ADMIN_EMAIL;
 const adminPassword = process.env.ADMIN_PASSWORD;
 const adminName = process.env.ADMIN_NAME || "Administrador SAM";

 if (!adminNif || !adminEmail || !adminPassword) {
  console.log("[SQL] admin: ADMIN_NIF, ADMIN_EMAIL ou ADMIN_PASSWORD não definidos, a ignorar");
  return;
 }

 // Ensure columns support admin entity (bcrypt hash + nullable iban)
 await sequelize.query("ALTER TABLE `entidade` MODIFY COLUMN `password` VARCHAR(255) NOT NULL");
 await sequelize.query("ALTER TABLE `entidade` MODIFY COLUMN `iban` VARCHAR(23) NULL");

 const hashedPassword = await bcrypt.hash(adminPassword, 10);

 // Remove any existing admin row (safe after clear or on re-seed without clear)
 await queryInterface.bulkDelete("entidade", { nif_nipc: adminNif }, {});

 await queryInterface.bulkInsert("entidade", [{
  nif_nipc: adminNif,
  email_login: adminEmail,
  password: hashedPassword,
  nome_entidade: adminName,
  iban: null,
  role: "admin",
 }], {});

 console.log(`[SQL] admin: entidade criada (nif=${adminNif})`);
}

async function main() {
 const queryInterface = sequelize.getQueryInterface();

 try {
  await sequelize.authenticate();

  if (SHOULD_CLEAR) {
   await clearTables(queryInterface);
  }

  for (const step of seedPlan) {
   if (!step.file) continue; // clear-only entries (e.g. leads)
   await seedTable(queryInterface, step);
  }

  await seedLeads(queryInterface);
  await fixAutoIncrements(queryInterface);
  await fixLeadsIdItem();
  await seedAdmin(queryInterface);
 } finally {
  await sequelize.close();
 }
}

main().catch((error) => {
 console.error("[SQL] erro ao importar dados:", error);
 process.exit(1);
});
