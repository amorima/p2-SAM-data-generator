"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.changeColumn("entidade", "password", {
   type: Sequelize.STRING(255),
   allowNull: false,
  });
 },

 async down(queryInterface, Sequelize) {
  await queryInterface.changeColumn("entidade", "password", {
   type: Sequelize.STRING(45),
   allowNull: false,
  });
 },
};
