"use strict";

module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.changeColumn("doacao", "id_doacao", {
      type: Sequelize.INTEGER,
      primaryKey: true,
      autoIncrement: true,
      allowNull: false,
    });
  },

  async down(queryInterface, Sequelize) {
    await queryInterface.changeColumn("doacao", "id_doacao", {
      type: Sequelize.INTEGER,
      primaryKey: true,
      allowNull: false,
    });
  },
};
