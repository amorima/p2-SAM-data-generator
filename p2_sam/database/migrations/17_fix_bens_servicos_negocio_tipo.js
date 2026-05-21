"use strict";

module.exports = {
 async up(queryInterface, Sequelize) {
  await queryInterface.changeColumn("bens_e_servicos_negocio", "tipo_bem_servico", {
   type: Sequelize.STRING(50),
   allowNull: false,
  });
 },

 async down(queryInterface, Sequelize) {
  await queryInterface.changeColumn("bens_e_servicos_negocio", "tipo_bem_servico", {
   type: Sequelize.STRING(10),
   allowNull: false,
  });
 },
};
