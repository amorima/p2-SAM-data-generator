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
   blocked: {
    type: Sequelize.TINYINT,
    allowNull: false,
    defaultValue: 0,
   },
   role: {
    type: Sequelize.STRING(255),
    allowNull: false,
    defaultValue: "citizen",
   },
   reason: {
    type: Sequelize.STRING(255),
    allowNull: true,
    defaultValue: null,
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("cidadao");
 },
};
