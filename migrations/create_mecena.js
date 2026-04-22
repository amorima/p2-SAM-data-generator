"use strict";

module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable("mecena", {
      nif_nipc: {
        type: Sequelize.STRING(9),
        primaryKey: true,
        allowNull: false,
        references: { model: "entidade", key: "nif_nipc" },
        onDelete: "CASCADE",
      },
    });
  },

  async down(queryInterface) {
    await queryInterface.dropTable("mecena");
  },
};