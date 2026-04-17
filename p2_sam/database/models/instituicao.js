const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Instituicao = sequelize.define(
  "instituicao",
  {
   nif_nipc: {
    type: DataTypes.STRING(20),
    primaryKey: true,
   },
   geo_latitude: {
    type: DataTypes.DECIMAL(10, 8),
    allowNull: false,
   },
   geo_longitude: {
    type: DataTypes.DECIMAL(11, 8),
    allowNull: false,
   },
   url_comprovativo_estatuto: {
    type: DataTypes.TEXT,
    allowNull: false,
   },
  },
  {
   tableName: "instituicao",
   timestamps: false,
  }
 );

 Instituicao.associate = (models) => {
  // Cada pode ter varios pedidos
  Instituicao.hasMany(models.Pedido, {
   foreignKey: "nif_nipc",
   as: "pedido",
  });
 };

 return Instituicao;
};
