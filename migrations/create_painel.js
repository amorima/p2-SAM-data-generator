"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("painel", {
   id_dispositivo: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    allowNull: false,
    autoIncrement: true,
   },
   token_api: {
    type: Sequelize.STRING(255),
    allowNull: false,
    unique: true,
   },
   geo_latitude: {
    type: Sequelize.DECIMAL(10, 8),
    allowNull: false,
   },
   geo_longitude: {
    type: Sequelize.DECIMAL(11, 8),
    allowNull: false,
   },
   raio_alcance: {
    type: Sequelize.INTEGER,
    allowNull: false,
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("painel");
 },
};
