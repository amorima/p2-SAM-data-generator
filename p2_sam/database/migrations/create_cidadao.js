"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("cidadao", {
   nome: {
    type: Sequelize.STRING(50),
    primaryKey: true,
    allowNull: false,
   },
   contacto: {
    type: Sequelize.STRING(13),
    allowNull: false,
    unique: true,
   },
   rgpd: {
    type: Sequelize.TINYINT,
    allowNull: false,
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("cidadao");
 },
};
