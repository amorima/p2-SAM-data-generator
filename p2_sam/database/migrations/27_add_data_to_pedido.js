"use strict";

module.exports = {
 async up(queryInterface) {
  const [[{ cnt }]] = await queryInterface.sequelize.query(`
   SELECT COUNT(*) as cnt
   FROM INFORMATION_SCHEMA.COLUMNS
   WHERE TABLE_SCHEMA = DATABASE()
     AND TABLE_NAME = 'pedido'
     AND COLUMN_NAME = 'data'
  `);
  // Raw ALTER: Sequelize's addColumn drops the literal CURRENT_TIMESTAMP default
  // for DATETIME columns, leaving the column NOT NULL without a default.
  if (cnt === 0) {
   await queryInterface.sequelize.query(
    "ALTER TABLE `pedido` ADD COLUMN `data` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP"
   );
  }
 },

 async down(queryInterface) {
  await queryInterface.removeColumn("pedido", "data");
 },
};
