"use strict";

module.exports = {
  async up(queryInterface) {
    const sequelize = queryInterface.sequelize;

    // Drop existing composite FK from leads (may not exist if migration 16 partially ran)
    try {
      await sequelize.query("ALTER TABLE `leads` DROP FOREIGN KEY `fk_leads_pedido_bens_e_servicos`");
    } catch {
      // FK did not exist — continue
    }

    // Replace composite PK with surrogate id_item
    await sequelize.query("ALTER TABLE `pedido_bens_e_servicos` DROP PRIMARY KEY");
    await sequelize.query("ALTER TABLE `pedido_bens_e_servicos` ADD COLUMN `id_item` INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST");
    await sequelize.query("ALTER TABLE `pedido_bens_e_servicos` ADD UNIQUE KEY `uq_pbs_pedido_item` (`id_pedido`, `tipo_bem_servico`)");

    // Add id_item FK column to leads (nullable so existing rows are not broken)
    await sequelize.query("ALTER TABLE `leads` ADD COLUMN `id_item` INT NULL");

    // Populate id_item in existing leads rows from the matching pedido_bens_e_servicos row
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
