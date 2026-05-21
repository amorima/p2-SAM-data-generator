"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.changeColumn("leads", "contacto_cidadao", {
   type: Sequelize.STRING(50),
   allowNull: true,
  });
 },

 async down(queryInterface, Sequelize) {
  await queryInterface.changeColumn("leads", "contacto_cidadao", {
   type: Sequelize.STRING(50),
   allowNull: false,
  });
 },
};
