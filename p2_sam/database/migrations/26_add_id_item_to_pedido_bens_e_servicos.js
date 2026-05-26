"use strict";

async function columnExists(queryInterface, table, column) {
  const [[{ cnt }]] = await queryInterface.sequelize.query(`
    SELECT COUNT(*) as cnt
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = :table
      AND COLUMN_NAME = :column
  `, { replacements: { table, column } });
  return cnt > 0;
}

module.exports = {
  async up(queryInterface) {
    const sequelize = queryInterface.sequelize;

    // Drop existing composite FK from leads (may not exist)
    try {
      await sequelize.query("ALTER TABLE `leads` DROP FOREIGN KEY `fk_leads_pedido_bens_e_servicos`");
    } catch {
      // FK did not exist — continue
    }

    // Only restructure pedido_bens_e_servicos if id_item doesn't exist yet
    const pbsHasIdItem = await columnExists(queryInterface, "pedido_bens_e_servicos", "id_item");
    if (!pbsHasIdItem) {
      await sequelize.query("ALTER TABLE `pedido_bens_e_servicos` DROP PRIMARY KEY");
      await sequelize.query("ALTER TABLE `pedido_bens_e_servicos` ADD COLUMN `id_item` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST");
      await sequelize.query("ALTER TABLE `pedido_bens_e_servicos` ADD UNIQUE KEY `uq_pbs_pedido_item` (`id_pedido`, `tipo_bem_servico`)");
    }

    // Only add id_item to leads if it doesn't exist yet
    const leadsHasIdItem = await columnExists(queryInterface, "leads", "id_item");
    if (!leadsHasIdItem) {
      await sequelize.query("ALTER TABLE `leads` ADD COLUMN `id_item` INT NULL");
    }

    // Populate id_item in leads from matching pedido_bens_e_servicos rows
    await sequelize.query(`
      UPDATE leads l
      INNER JOIN pedido_bens_e_servicos pbs
        ON pbs.id_pedido = l.id_pedido AND pbs.tipo_bem_servico = l.item_pedido
      SET l.id_item = pbs.id_item
      WHERE l.id_item IS NULL
    `);

    // Add FK from leads.id_item → pedido_bens_e_servicos.id_item
    try {
      await sequelize.query(`
        ALTER TABLE \`leads\`
        ADD CONSTRAINT \`fk_leads_pbs_id_item\`
        FOREIGN KEY (\`id_item\`) REFERENCES \`pedido_bens_e_servicos\` (\`id_item\`)
        ON DELETE SET NULL ON UPDATE CASCADE
      `);
    } catch (e) {
      console.warn(`[migration 26] Could not add FK: ${e.message}`);
    }
  },

  async down(queryInterface) {
    const sequelize = queryInterface.sequelize;

    try {
      await sequelize.query("ALTER TABLE `leads` DROP FOREIGN KEY `fk_leads_pbs_id_item`");
    } catch { /* ignore */ }

    await sequelize.query("ALTER TABLE `leads` DROP COLUMN `id_item`");

    try {
      await sequelize.query("ALTER TABLE `pedido_bens_e_servicos` DROP INDEX `uq_pbs_pedido_item`");
    } catch { /* ignore */ }

    await sequelize.query("ALTER TABLE `pedido_bens_e_servicos` DROP COLUMN `id_item`");
    await sequelize.query("ALTER TABLE `pedido_bens_e_servicos` ADD PRIMARY KEY (`id_pedido`, `tipo_bem_servico`)");
  },
};
