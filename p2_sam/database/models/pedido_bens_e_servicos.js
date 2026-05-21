const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Pedido_Bens_E_Servicos = sequelize.define(
  "pedido_bens_e_servicos",
  {
   id_item: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
   },
   id_pedido: {
    type: DataTypes.INTEGER,
    allowNull: false,
   },
   tipo_bem_servico: {
    type: DataTypes.STRING(50),
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
  },
 );

 Pedido_Bens_E_Servicos.associate = (models) => {
  Pedido_Bens_E_Servicos.belongsTo(models.Pedido, {
   foreignKey: "id_pedido",
   as: "pedido",
  });
  Pedido_Bens_E_Servicos.belongsTo(models.Bens_E_Servico, {
   foreignKey: "tipo_bem_servico",
   as: "bens_e_servico",
  });
  Pedido_Bens_E_Servicos.hasMany(models.Lead, {
   foreignKey: "id_pedido",
   sourceKey: "id_pedido",
   as: "leads",
  });
 };

 return Pedido_Bens_E_Servicos;
};
