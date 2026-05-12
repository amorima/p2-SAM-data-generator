const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Cidadao = sequelize.define(
  "cidadao",
  {
   nome: {
    type: DataTypes.STRING(50),
    primaryKey: true,
   },
   contacto: {
    type: DataTypes.STRING(13),
    allowNull: false,
   },
   rgpd: {
    type: DataTypes.TINYINT,
    allowNull: false,
   },
  },
  {
   tableName: "cidadao",
   timestamps: false,
  },
 );

 Cidadao.associate = (models) => {
  Cidadao.hasMany(models.Lead, {
   foreignKey: "nome_cidadao",
   sourceKey: "nome",
   as: "leads",
  });
 };

 return Cidadao;
};
