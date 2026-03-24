const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Pedido_Bens_E_Servicos = sequelize.define(
  "pedido_bens_e_servicos",
  {
   id_pedido: {
    type: DataTypes.INTEGER,
    primarykey: true,
    autoIncrement: true,
    allowNull: false,
    unique: true,
   },
   tipo_bem_servico: {
    type: DataTypes.STRING(100),
    allowNull: false,
   },
   publico: {
    type: DataTypes.TINYINT,
    allowNull: false,
   },
  },
  {
   tableName: "pedido_bens_e_servicos",
   timestamps: false,
  }
 );

 Pedido_Bens_E_Servicos.associate = (models) => {
  // Cada doação pertence a um mecenas
  Pedido_Bens_E_Servicos.hasOne(models.Pedido, {
   foreignKey: "id_pedido",
   as: "pedido",
  });
  Pedido_Bens_E_Servicos.hasOne(models.Bens_E_Servico, {
   foreignKey: "tipo_bem_servico",
   as: "bens_e_servico",
  });
  Pedido_Bens_E_Servicos.hasOne(models.Lead, {
   foreignKey: "id_pedido",
   as: "lead",
  });
 };

 return Pedido_Bens_E_Servicos;
};
