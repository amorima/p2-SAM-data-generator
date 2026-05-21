"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.sequelize.query("SET FOREIGN_KEY_CHECKS = 0");
  await queryInterface.sequelize.query(
   "ALTER TABLE pedido MODIFY COLUMN id_pedido INT NOT NULL AUTO_INCREMENT"
  );
  await queryInterface.sequelize.query("SET FOREIGN_KEY_CHECKS = 1");
  await queryInterface.addColumn("pedido", "urgente", {
   type: Sequelize.BOOLEAN,
   allowNull: false,
   defaultValue: false,
  });
 },

 async down(queryInterface, Sequelize) {
  await queryInterface.removeColumn("pedido", "urgente");
  await queryInterface.sequelize.query("SET FOREIGN_KEY_CHECKS = 0");
  await queryInterface.sequelize.query(
   "ALTER TABLE pedido MODIFY COLUMN id_pedido INT NOT NULL"
  );
  await queryInterface.sequelize.query("SET FOREIGN_KEY_CHECKS = 1");
 },
};
