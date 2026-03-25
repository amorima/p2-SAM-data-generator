const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Localidade = sequelize.define(
  "Localidade",
  {
   codigo_postal: {
    type: DataTypes.STRING(45),
    primaryKey: true,
   },
   concelho: {
    type: DataTypes.STRING(45),
    allowNull: false,
   },
   pais: {
    type: DataTypes.STRING(45),
    allowNull: false,
   },
  },
  {
   tableName: "localidade",
   timestamps: false,
  }
 );

 Localidade.associate = (models) => {
  Localidade.belongsToMany(models.Entidade, {
   through: models.Localidade_Entidade,
   foreignKey: "localidade_codigo_postal",
   as: "entidades",
  });
 };

 return Localidade;
};
