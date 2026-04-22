"use strict";

module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable("instituicao", {
      nif_nipc: {
        type: Sequelize.STRING(9),
        primaryKey: true,
        allowNull: false,
        onDelete: "CASCADE",
      },
      geo_latitude: {
       type: Sequelize.DECIMAL(10, 8),
       allowNull: false,
      },
      geo_longitude: {
       type: Sequelize.DECIMAL(11, 8),
       allowNull: false,
      },
      url_comprovativo_estatuto: {
       type: Sequelize.TEXT,
       allowNull: false,
      },
    });
  },

  async down(queryInterface) {
    await queryInterface.dropTable("instituicao");
  },
};