const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Localidade_Entidade = sequelize.define(
  "localidade_entidade",
  {
   entidade_nif_nipc: {
    type: DataTypes.STRING(45),
    primaryKey: true,
   },
   localidade_codigo_postal: {
    type: DataTypes.STRING(45),
    primaryKey: true,
   },
  },
  {
   tableName: "localidade_entidade",
   timestamps: false,
  }
 );

 Localidade_Entidade.associate = (models) => {
  // Cada localidade pertence a um mecenas
  Localidade_Entidade.belongsTo(models.Localidade, {
   foreignKey: "localidade_codigo_postal",
   as: "localidade_entidade",
  });
  Localidade_Entidade.belongsTo(models.Entidade, {
   foreignKey: "entidade_nif_nipc",
   as: "entidade",
  });
 };

 return Localidade_Entidade;
};
