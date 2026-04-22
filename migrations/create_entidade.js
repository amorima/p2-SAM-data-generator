"use strict";

module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable("entidade", {
      nif_nipc: {
        type: Sequelize.STRING(9),
        primaryKey: true,
        allowNull: false,
        onDelete: "CASCADE",
      },
      email_login: {
       type: Sequelize.STRING(45),
       allowNull: false,
      },
      password: {
       type: Sequelize.STRING(45),
       allowNull: false,
      },
      nome_entidade: {
       type: Sequelize.STRING(45),
       allowNull: false,
      },
      iban: {
       type: Sequelize.STRING(23),
       allowNull: false,
       unique: true,
      },
      codigo_postal: {
       type: Sequelize.STRING(8),
       allowNull: false,
      },
    });
  },

  async down(queryInterface) {
    await queryInterface.dropTable("entidade");
  },
};