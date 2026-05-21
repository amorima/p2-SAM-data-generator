"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.changeColumn("pedido_bens_e_servicos", "publico", {
   type: Sequelize.TINYINT,
   allowNull: true,
  });
 },

 async down(queryInterface, Sequelize) {
  await queryInterface.changeColumn("pedido_bens_e_servicos", "publico", {
   type: Sequelize.TINYINT,
   allowNull: false,
  });
 },
};
