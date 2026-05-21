"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.changeColumn("entidade", "codigo_postal", {
   type: Sequelize.STRING(8),
   allowNull: true,
  });
 },

 async down(queryInterface, Sequelize) {
  await queryInterface.changeColumn("entidade", "codigo_postal", {
   type: Sequelize.STRING(8),
   allowNull: false,
  });
 },
};
