const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Instituicao = sequelize.define(
  "instituicao",
  {
   nif_nipc: {
    type: DataTypes.STRING(20),
    primarykey: true,
   },
   geo_latitude: {
    type: DataTypes.DECIMAL(10, 8),
    allowNull: false,
   },
   geo_longitude: {
    type: DataTypes.DECIMAL(11, 8),
    allowNull: false,
   },
   url_certidao_estatuto: {
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
  // Cada doação pertence a um mecenas
  Instituicao.hasMany(models.Pedido, {
   foreignKey: "nif_nipc",
   as: "pedido",
  });
 };

 return Instituicao;
};
