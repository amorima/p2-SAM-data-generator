"use strict";

module.exports = {
 async up(queryInterface) {
  await queryInterface.sequelize.query(
   "ALTER TABLE `entidade` MODIFY COLUMN `iban` VARCHAR(23) NULL"
  );
 },

 async down(queryInterface) {
  await queryInterface.sequelize.query(
   "ALTER TABLE `entidade` MODIFY COLUMN `iban` VARCHAR(23) NOT NULL"
  );
 },
};
