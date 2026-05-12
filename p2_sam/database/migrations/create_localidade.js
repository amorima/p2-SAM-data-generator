"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("localidade", {
   codigo_postal: {
    type: Sequelize.STRING(8),
    primaryKey: true,
    allowNull: false,
   },
   concelho: {
    type: Sequelize.STRING(45),
    allowNull: false,
   },
   distrito: {
    type: Sequelize.STRING(45),
    allowNull: false,
   },
   freguesia: {
    type: Sequelize.STRING(45),
    allowNull: false,
   },
   pais: {
    type: Sequelize.STRING(45),
    allowNull: false,
   },
   rua: {
    type: Sequelize.STRING(45),
    allowNull: false,
   },
   n_porta: {
    type: Sequelize.STRING(5),
    allowNull: false,
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("localidade");
 },
};
