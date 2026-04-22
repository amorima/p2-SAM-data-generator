"use strict";

module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable("bens_e_servico", {
      tipo_bem_servico: {
        type: Sequelize.STRING(10),
        primaryKey: true,
        allowNull: false,
        onDelete: "CASCADE",
      },
      tipo_bem: {
       type: Sequelize.ENUM("alimentação", "vestuario", "higiene", "educação", "saude", "transporte", "habitacao", "outro"),
       allowNull: false,
      }
    });
  },

  async down(queryInterface) {
    await queryInterface.dropTable("bens_e_servico");
  },
};