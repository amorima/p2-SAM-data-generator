const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Pedido = sequelize.define(
  "pedido",
  {
   id_pedido: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    unique: true,
   },
   nif_nipc: {
    type: DataTypes.STRING(9),
    allowNull: false,
   },
   estado: {
    type: DataTypes.ENUM("PENDENTE", "ACEITE", "REJEITADO"),
    allowNull: false,
   },
   data: {
    type: DataTypes.DATE,
    allowNull: false,
    defaultValue: DataTypes.NOW,
   },
  },
  {
   tableName: "pedido",
   timestamps: false,
  },
 );

 Pedido.associate = (models) => {
  // Cada doação pertence a um mecenas
  Pedido.belongsTo(models.Instituicao, {
   foreignKey: "nif_nipc",
   as: "instituicao",
  });
  Pedido.hasMany(models.Pedido_Bens_E_Servicos, {
   foreignKey: "id_pedido",
   as: "pedido_bens",
  });
 };

 return Pedido;
};
