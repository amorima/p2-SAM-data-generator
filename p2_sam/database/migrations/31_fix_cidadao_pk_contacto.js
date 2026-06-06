"use strict";

// A migration 03 definiu 'nome' como PK mas o modelo Sequelize usa 'contacto'.
// Esta migration corrige a inconsistência: troca a PK para 'contacto', que é o
// identificador único real do cidadão (nº telemóvel / email).
module.exports = {
  async up(queryInterface) {
    const sq = queryInterface.sequelize;

    // 1 — Remover FK de leads.nome_cidadao → cidadao.nome (se existir)
    const [nomeFks] = await sq.query(`
      SELECT CONSTRAINT_NAME
      FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
      WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'leads'
        AND COLUMN_NAME = 'nome_cidadao'
        AND REFERENCED_TABLE_NAME = 'cidadao'
    `);
    for (const { CONSTRAINT_NAME } of nomeFks) {
      await sq.query(`ALTER TABLE \`leads\` DROP FOREIGN KEY \`${CONSTRAINT_NAME}\``);
    }

    // 2 — Remover FK de leads.contacto_cidadao → cidadao.contacto (temporariamente)
    const [contactoFks] = await sq.query(`
      SELECT CONSTRAINT_NAME
      FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
      WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'leads'
        AND COLUMN_NAME = 'contacto_cidadao'
        AND REFERENCED_TABLE_NAME = 'cidadao'
    `);
    for (const { CONSTRAINT_NAME } of contactoFks) {
      await sq.query(`ALTER TABLE \`leads\` DROP FOREIGN KEY \`${CONSTRAINT_NAME}\``);
    }

    // 3 — Trocar PK: nome → contacto
    await sq.query("ALTER TABLE `cidadao` DROP PRIMARY KEY");
    await sq.query("ALTER TABLE `cidadao` ADD INDEX `idx_cidadao_nome` (`nome`)");

    // Remover unique index em contacto (passa a ser PK)
    const [uqRows] = await sq.query(`
      SELECT INDEX_NAME
      FROM INFORMATION_SCHEMA.STATISTICS
      WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'cidadao'
        AND COLUMN_NAME = 'contacto'
        AND NON_UNIQUE = 0
        AND INDEX_NAME != 'PRIMARY'
    `);
    for (const { INDEX_NAME } of uqRows) {
      await sq.query(`ALTER TABLE \`cidadao\` DROP INDEX \`${INDEX_NAME}\``);
    }

    await sq.query("ALTER TABLE `cidadao` ADD PRIMARY KEY (`contacto`)");

    // 4 — Repor FK de leads.contacto_cidadao → cidadao.contacto (nova PK)
    try {
      await sq.query(`
        ALTER TABLE \`leads\`
        ADD CONSTRAINT \`fk_leads_contacto_cidadao\`
        FOREIGN KEY (\`contacto_cidadao\`) REFERENCES \`cidadao\` (\`contacto\`)
        ON DELETE CASCADE ON UPDATE CASCADE
      `);
    } catch (e) {
      console.warn("[migration 31] FK contacto_cidadao não recriada:", e.message);
    }
  },

  async down(queryInterface) {
    const sq = queryInterface.sequelize;

    // Inverter: contacto volta a UNIQUE, nome volta a PK
    const [fks] = await sq.query(`
      SELECT CONSTRAINT_NAME
      FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
      WHERE TABLE_SCHEMA = DATABASE()
        AND TABLE_NAME = 'leads'
        AND COLUMN_NAME = 'contacto_cidadao'
        AND REFERENCED_TABLE_NAME = 'cidadao'
    `);
    for (const { CONSTRAINT_NAME } of fks) {
      await sq.query(`ALTER TABLE \`leads\` DROP FOREIGN KEY \`${CONSTRAINT_NAME}\``);
    }

    await sq.query("ALTER TABLE `cidadao` DROP PRIMARY KEY");
    await sq.query("ALTER TABLE `cidadao` ADD UNIQUE (`contacto`)");

    try {
      await sq.query("ALTER TABLE `cidadao` DROP INDEX `idx_cidadao_nome`");
    } catch { /* ignore */ }

    await sq.query("ALTER TABLE `cidadao` ADD PRIMARY KEY (`nome`)");
  },
};
