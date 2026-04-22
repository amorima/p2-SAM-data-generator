"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("lead", {
   id_lead: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    allowNull: false,
    autoIncrement: true,
   },
   data: {
    type: Sequelize.DATE,
    allowNull: false,
   },
   id_painel: {
    type: Sequelize.INTEGER,
    allowNull: false,
    reference: { model: "painel", key: "id_dispositivo" },
    onDelete: "CASCADE",
   },
   nome_cidadao: {
    type: Sequelize.STRING(50),
    allowNull: false,
    reference: { model: "cidadao", key: "nome" },
    onDelete: "CASCADE",
   },
   contacto_cidadao: {
    type: Sequelize.STRING(13),
    allowNull: false,
    reference: { model: "cidadao", key: "contacto" },
    onDelete: "CASCADE",
   },
   id_pedido: {
    type: Sequelize.INTEGER,
    allowNull: false,
    reference: { model: "pedido_bens_e_servicos", key: "id_pedido" },
    onDelete: "CASCADE",
   },
   item_pedido: {
    type: Sequelize.STRING(100),
    allowNull: false,
    reference: { model: "pedido_bens_e_servicos", key: "tipo_bem_servico" },
    onDelete: "CASCADE",
   },
   estado: {
    type: Sequelize.ENUM("ENTREGUE", "PENDENTE", "EXPIRADO"),
    allowNull: false,
   },
   pin_entrega: {
    type: Sequelize.STRING(16),
    allowNull: false,
   },
   id_locker: {
    type: Sequelize.INTEGER,
    allowNull: false,
    reference: { model: "locker", key: "id_locker" },
    onDelete: "CASCADE",
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("lead");
 },
};
