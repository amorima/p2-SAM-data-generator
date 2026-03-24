const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const negocio = sequelize.define(
  "negocio",
  {
   nif_nipc: {
    type: DataTypes.STRING(9),
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
  // Cada negocio tem uma entidade e varias Bens_E_Servicos_Negocio
  negocio.hasOne(models.Entidade, {
   foreignKey: "nif_nipc",
   as: "entidade",
  });
  negocio.hasMany(models.Bens_E_Servicos_Negocio, {
   foreignKey: "negocio_nif_nipc",
   as: "bens_e_servicos_negocio",
  });
 };

 return Negocio;
};
