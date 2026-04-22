"use strict";

module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable("contacto", {
      contacto: {
        type: Sequelize.STRING(45),
        primaryKey: true,
        allowNull: false,
        onDelete: "CASCADE",
      },
      entidade_nif_nipc: {
       type: Sequelize.STRING(9),
       allowNull: false,
       reference: {model: "entidade", key: "nif_nipc"},
       onDelete: "CASCADE",
      },
      nome_contacto: {
       type: Sequelize.STRING(100),
       allowNull: false,
      },
      descricao: {
       type: Sequelize.STRING(255),
       allowNull: false,
      },
    });
  },

  async down(queryInterface) {
    await queryInterface.dropTable("contacto");
  },
};