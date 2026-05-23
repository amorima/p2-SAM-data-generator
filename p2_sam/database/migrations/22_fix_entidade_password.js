"use strict";

module.exports = {
 async up(queryInterface) {
  await queryInterface.sequelize.query(
   "ALTER TABLE `entidade` MODIFY COLUMN `password` VARCHAR(255) NOT NULL"
  );
 },

 async down(queryInterface) {
  await queryInterface.sequelize.query(
   "ALTER TABLE `entidade` MODIFY COLUMN `password` VARCHAR(45) NOT NULL"
  );
 },
};
