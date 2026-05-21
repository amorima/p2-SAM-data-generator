"use strict";

module.exports = {
  async up(queryInterface) {
    const sequelize = queryInterface.sequelize;
    await sequelize.query("ALTER TABLE `doacao` MODIFY `id_doacao` INT NOT NULL AUTO_INCREMENT");
    await sequelize.query("ALTER TABLE `leads` MODIFY `id_lead` INT NOT NULL AUTO_INCREMENT");
    await sequelize.query("ALTER TABLE `pedido` MODIFY `id_pedido` INT NOT NULL AUTO_INCREMENT");
  },

  async down(queryInterface) {
    const sequelize = queryInterface.sequelize;
    await sequelize.query("ALTER TABLE `doacao` MODIFY `id_doacao` INT NOT NULL");
    await sequelize.query("ALTER TABLE `leads` MODIFY `id_lead` INT NOT NULL");
    await sequelize.query("ALTER TABLE `pedido` MODIFY `id_pedido` INT NOT NULL");
  },
};
