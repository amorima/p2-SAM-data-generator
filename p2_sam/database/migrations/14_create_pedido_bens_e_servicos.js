"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("pedido_bens_e_servicos", {
   id_pedido: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    allowNull: false,
    references: { model: "pedido", key: "id_pedido" },
    onDelete: "CASCADE",
   },
   tipo_bem_servico: {
    type: Sequelize.STRING(50),
    primaryKey: true,
    allowNull: false,
    references: { model: "bens_e_servicos", key: "tipo_bem_servico" },
    onDelete: "CASCADE",
   },
   publico: {
    type: Sequelize.TINYINT,
    allowNull: false,
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("pedido_bens_e_servicos");
 },
};
