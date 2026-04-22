"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("localidade_entidade", {
   entidade_nif_nipc: {
    type: Sequelize.STRING(45),
    primaryKey: true,
    allowNull: false,
    reference: { model: "entidade", key: "nif_nipc" },
    onDelete: "CASCADE",
   },
   localidade_codigo_postal: {
    type: Sequelize.STRING(45),
    primaryKey: true,
    allowNull: false,
    reference: { model: "localidade", key: "codigo_postal" },
    onDelete: "CASCADE",
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("localidade_entidade");
 },
};
