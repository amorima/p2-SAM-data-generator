"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.changeColumn("entidade", "iban", {
   type: Sequelize.STRING(23),
   allowNull: true,
   unique: true,
  });
 },

 async down(queryInterface, Sequelize) {
  await queryInterface.changeColumn("entidade", "iban", {
   type: Sequelize.STRING(23),
   allowNull: false,
   unique: true,
  });
 },
};
