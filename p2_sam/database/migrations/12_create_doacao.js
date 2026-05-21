"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("doacao", {
   id_doacao: {
    type: Sequelize.INTEGER,
    primaryKey: true,
    autoIncrement: true,
    allowNull: false,
   },
   mecena_nif_nipc: {
    type: Sequelize.STRING(9),
    allowNull: false,
    references: { model: "mecena", key: "nif_nipc" },
    onDelete: "CASCADE",
   },
   data: {
    type: Sequelize.DATE,
    allowNull: false,
   },
   valor_transacao: {
    type: Sequelize.DECIMAL(10, 2),
    allowNull: false,
   },
   tipo_donativo: {
    type: Sequelize.ENUM("TRANSFERENCIA", "NUMERARIO", "CHEQUE", "REFERENCIA"),
    allowNull: false,
   },
   anonimo: {
    type: Sequelize.BOOLEAN,
    allowNull: false,
   },
   url_comprovativo: {
    type: Sequelize.TEXT,
    allowNull: false,
   },
   estado: {
    type: Sequelize.ENUM("ACEITE", "REJEITADO", "PENDENTE"),
    allowNull: false,
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("doacao");
 },
};
