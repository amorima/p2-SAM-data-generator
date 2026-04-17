const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Localidade = sequelize.define(
  "Localidade",
  {
   codigo_postal: {
    type: DataTypes.STRING(8),
    primaryKey: true,
   },
   concelho: {
    type: DataTypes.STRING(45),
    allowNull: false,
   },
   distrito: {
    type: DataTypes.STRING(45),
    allowNull: false,
   },
   freguesia: {
    type: DataTypes.STRING(45),
    allowNull: false,
   },
   pais: {
    type: DataTypes.STRING(45),
    allowNull: false,
   },
   rua: {
    type: DataTypes.STRING(200),
    allowNull: false,
   },
   n_porta: {
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
