"use strict";

module.exports = {
 async up(queryInterface) {
  const [[{ cnt }]] = await queryInterface.sequelize.query(`
   SELECT COUNT(*) as cnt
   FROM INFORMATION_SCHEMA.COLUMNS
   WHERE TABLE_SCHEMA = DATABASE()
     AND TABLE_NAME = 'pedido_bens_e_servicos'
     AND COLUMN_NAME = 'publico'
  `);
  if (cnt > 0) {
   await queryInterface.sequelize.query(
    "ALTER TABLE `pedido_bens_e_servicos` MODIFY COLUMN `publico` TINYINT NULL"
   );
  }
 },

 async down(queryInterface) {
  const [[{ cnt }]] = await queryInterface.sequelize.query(`
   SELECT COUNT(*) as cnt
   FROM INFORMATION_SCHEMA.COLUMNS
   WHERE TABLE_SCHEMA = DATABASE()
     AND TABLE_NAME = 'pedido_bens_e_servicos'
     AND COLUMN_NAME = 'publico'
  `);
  if (cnt > 0) {
   await queryInterface.sequelize.query(
    "ALTER TABLE `pedido_bens_e_servicos` MODIFY COLUMN `publico` TINYINT NOT NULL"
   );
  }
 },
};
