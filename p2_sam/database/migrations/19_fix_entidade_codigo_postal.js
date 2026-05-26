"use strict";

module.exports = {
 async up(queryInterface) {
  const [[{ cnt }]] = await queryInterface.sequelize.query(`
   SELECT COUNT(*) as cnt
   FROM INFORMATION_SCHEMA.COLUMNS
   WHERE TABLE_SCHEMA = DATABASE()
     AND TABLE_NAME = 'entidade'
     AND COLUMN_NAME = 'codigo_postal'
  `);
  if (cnt > 0) {
   await queryInterface.sequelize.query(
    "ALTER TABLE `entidade` MODIFY COLUMN `codigo_postal` VARCHAR(8) NULL"
   );
  }
 },

 async down(queryInterface) {
  const [[{ cnt }]] = await queryInterface.sequelize.query(`
   SELECT COUNT(*) as cnt
   FROM INFORMATION_SCHEMA.COLUMNS
   WHERE TABLE_SCHEMA = DATABASE()
     AND TABLE_NAME = 'entidade'
     AND COLUMN_NAME = 'codigo_postal'
  `);
  if (cnt > 0) {
   await queryInterface.sequelize.query(
    "ALTER TABLE `entidade` MODIFY COLUMN `codigo_postal` VARCHAR(8) NOT NULL"
   );
  }
 },
};
