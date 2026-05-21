"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("leads", {
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
    references: { model: "painel", key: "id_dispositivo" },
    onDelete: "CASCADE",
   },
   nome_cidadao: {
    type: Sequelize.STRING(50),
    allowNull: false,
    references: { model: "cidadao", key: "nome" },
    onDelete: "CASCADE",
   },
   contacto_cidadao: {
    type: Sequelize.STRING(50),
    allowNull: false,
    references: { model: "cidadao", key: "contacto" },
    onDelete: "CASCADE",
   },
   id_pedido: {
    type: Sequelize.INTEGER,
    allowNull: false,
   },
   item_pedido: {
    type: Sequelize.STRING(50),
    allowNull: false,
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
    references: { model: "locker_inteligente", key: "id_locker" },
    onDelete: "CASCADE",
   },
  });

  // Garante que existe um índice composto em pedido_bens_e_servicos
  // (pode já ter sido criada pelo back-end sem esse índice)
  try {
   await queryInterface.addIndex("pedido_bens_e_servicos", {
    fields: ["id_pedido", "tipo_bem_servico"],
    name: "idx_pbs_composite",
   });
  } catch (err) {
   if (!err.message.includes("Duplicate key name")) throw err;
  }

  await queryInterface.addConstraint("leads", {
   fields: ["id_pedido", "item_pedido"],
   type: "foreign key",
   name: "fk_leads_pedido_bens_e_servicos",
   references: {
    table: "pedido_bens_e_servicos",
    fields: ["id_pedido", "tipo_bem_servico"],
   },
   onDelete: "CASCADE",
   onUpdate: "CASCADE",
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("leads");
 },
};
