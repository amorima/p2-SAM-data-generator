const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Bens_E_Servico = sequelize.define(
  "bens_e_servico",
  {
   tipo_bem_servico: {
    type: DataTypes.STRING(10),
    primaryKey: true,
   },
   tipo_bem: {
    type: DataTypes.ENUM("alimentação", "vestuario", "higiene", "educação", "saude", "transporte", "habitacao", "outro"),
    allowNull: false,
   },
  },
  {
   tableName: "bens_e_servico",
   timestamps: false,
  }
 );

 Bens_E_Servico.associate = (models) => {
  // Cada Bens_E_Servico tem varios Bens_E_Servicos_Negocio e Pedido_Bens_E_Servicos
  Bens_E_Servico.hasMany(models.Bens_E_Servicos_Negocio, {
   foreignKey: "tipo_bem_servico",
   as: "bens_e_servicos_negocio",
  });
  Bens_E_Servico.hasMany(models.Pedido_Bens_E_Servicos, {
   foreignKey: "tipo_bem_servico",
   as: "pedido_bens_servicos",
  });
 };

 return Bens_E_Servico;
};
