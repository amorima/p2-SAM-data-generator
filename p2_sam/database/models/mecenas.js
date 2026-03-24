const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Mecena = sequelize.define(
  "Mecena",
  {
   nif_nipc: {
    type: DataTypes.INTEGER(9),
    primaryKey: true,
    allowNull: false,
   },
  },
  {
   tableName: "mecena",
   timestamps: false,
  }
 );

 Mecena.associate = (models) => {
  // Mecena pertence a uma Entidade (herança — partilha o nif_nipc)
  Mecena.belongsTo(models.Entidade, {
   foreignKey: "nif_nipc",
   as: "entidade",
  });

  // Mecena faz várias Doações
  Mecena.hasMany(models.Doacao, {
   foreignKey: "mecena_nif_nipc",
   as: "doacoes",
  });
 };

 return Mecena;
};
