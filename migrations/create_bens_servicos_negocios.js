"use strict";

module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable("bens_e_servico_negocio", {
      id_oferta: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        allowNull: false,
        onDelete: "CASCADE",
      },
      negocio_nif_nipc: {
       type: Sequelize.STRING(9),
       allowNull: false,
       reference: {model: "negocio", key: "nif_nipc"},
       onDelete: "CASCADE",
      },
      tipo_bem_servico: {
       type: Sequelize.STRING(10),
       allowNull: false,
       reference: {model: "bens_e_servico", key: "tipo_bem_servico"}
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
    await queryInterface.dropTable("bens_e_servico_negocio");
  },
};