"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("locker_inteligente", {
   id_locker: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    allowNull: false,
    autoIncrement: true,
   },
   estado: {
    type: Sequelize.ENUM("DISPONIVEL", "INDISPONIVEL", "OCUPADO", "MANUTENCAO"),
    allowNull: false,
   },
   codigo_mestre: {
    type: Sequelize.STRING(45),
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
   codigo_mestre: {
    type: Sequelize.STRING(45),
    allowNull: false,
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("locker_inteligente");
 },
};
