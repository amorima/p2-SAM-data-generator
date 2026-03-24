const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Localidade = sequelize.define(
  "Localidade",
  {
   codigo_postal: {
    type: DataTypes.STRING(45),
    primarykey: true,
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
  // Cada localidade pertence a um mecenas
  // ALTERAR POIS CADA LOCALIDADE PODE TER MAIS DE UM MECENAS E VICE VERSA
  Localidade.belongsTo(models.Mecena, {
   foreignKey: "mecena_nif_nipc",
   as: "mecena",
  });
 };

 return Localidade;
};
