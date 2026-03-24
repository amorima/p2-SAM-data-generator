const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const negocio = sequelize.define(
  "negocio",
  {
   nif_nipc: {
    type: DataTypes.STRING(9),
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
   url_certidao_permanente: {
    type: DataTypes.TEXT,
    allowNull: false,
   },
   inicio_atividade: {
    type: DataTypes.DATE,
    allowNull: false,
   },
  },
  {
   tableName: "negocio",
   timestamps: false,
  }
 );

 negocio.associate = (models) => {
  // Cada doação pertence a um mecenas
  negocio.belongsTo(models.tb, {
   foreignKey: "",
   as: "",
  });
 };

 return Negocio;
};
