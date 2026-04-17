const { DataTypes } = require("sequelize");

module.exports = (sequelize) => {
  const Painel = sequelize.define(
    "Painel",
    {
      id_dispositivo: {
        type: DataTypes.INTEGER,
        primaryKey: true,
        autoIncrement: true,
      },
      token_api: {
        type: DataTypes.STRING(255),
        allowNull: false,
        unique: true,
      },
      geo_latitude: {
        type: DataTypes.DECIMAL(10, 8),
        allowNull: false,
      },
      geo_longitude: {
        type: DataTypes.DECIMAL(11, 8),
        allowNull: false,
      },
      raio_alcance: {
        type: DataTypes.INTEGER,
        allowNull: false,
      },
    },
    {
      tableName: "painel",
      timestamps: false,
    }
  );

  Painel.associate = (models) => {
    Painel.hasMany(models.Lead, {
      foreignKey: "id_painel",
      as: "leads",
    });
  };

  return Painel;
};