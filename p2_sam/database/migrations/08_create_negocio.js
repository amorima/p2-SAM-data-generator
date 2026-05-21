"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("negocio", {
   nif_nipc: {
    type: Sequelize.STRING(9),
    primaryKey: true,
    allowNull: false,
   },
   geo_latitude: {
    type: Sequelize.DECIMAL(10, 8),
    allowNull: false,
   },
   geo_longitude: {
    type: Sequelize.DECIMAL(11, 8),
    allowNull: false,
   },
   url_certidao_permanente: {
    type: Sequelize.TEXT,
    allowNull: false,
   },
   inicio_atividade: {
    type: Sequelize.DATE,
    allowNull: false,
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("negocio");
 },
};
