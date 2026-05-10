"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("bens_e_servicos_negocio", {
   id_oferta: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    allowNull: false,
    autoIncrement: true,
   },
   negocio_nif_nipc: {
    type: Sequelize.STRING(9),
    allowNull: false,
    references: { model: "negocio", key: "nif_nipc" },
    onDelete: "CASCADE",
   },
   tipo_bem_servico: {
    type: Sequelize.STRING(50),
    allowNull: false,
    references: { model: "bens_e_servicos", key: "tipo_bem_servico" },
    onDelete: "CASCADE",
   },
   descricao: {
    type: Sequelize.STRING(255),
    allowNull: false,
   },
   valor_total: {
    type: Sequelize.DECIMAL(10, 2),
    allowNull: false,
   },
   desconto: {
    type: Sequelize.DECIMAL(10, 2),
    allowNull: false,
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("bens_e_servicos_negocio");
 },
};
