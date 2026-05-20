"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("pedido", {
   id_pedido: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    allowNull: false,
   },
   nif_nipc: {
    type: Sequelize.STRING(9),
    allowNull: false,
    references: { model: "instituicao", key: "nif_nipc" },
   },
   estado: {
    type: Sequelize.ENUM("PENDENTE", "ACEITE", "REJEITADO"),
    allowNull: false,
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("pedido");
 },
};
