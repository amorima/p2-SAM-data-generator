"use strict";

module.exports = {
 async up(queryInterface) {
  await queryInterface.sequelize.query(
   "ALTER TABLE `leads` MODIFY COLUMN `contacto_cidadao` VARCHAR(50) NULL"
  );
 },

 async down(queryInterface) {
  await queryInterface.sequelize.query(
   "ALTER TABLE `leads` MODIFY COLUMN `contacto_cidadao` VARCHAR(50) NOT NULL"
  );
 },
};
