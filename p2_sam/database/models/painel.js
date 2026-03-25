const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
 const Painel = sequelize.define(
  "t",
  {
   codigo_postal: {
    type: DataTypes.STRING(45),
    primaryKey: true,
   },
  },
  {
   tableName: "",
   timestamps: false,
  }
 );

 Painel.associate = (models) => {
  //
  Painel.belongsTo(models.tb, {
   foreignKey: "",
   as: "",
  });
 };

 return Painel;
};
