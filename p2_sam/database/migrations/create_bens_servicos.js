"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.createTable("bens_e_servicos", {
   tipo_bem_servico: {
    type: Sequelize.STRING(50),
    primaryKey: true,
    allowNull: false,
   },
   tipo: {
    type: Sequelize.ENUM("bem", "servico"),
    allowNull: false,
   },
  });
 },

 async down(queryInterface) {
  await queryInterface.dropTable("bens_e_servicos");
 },
};
