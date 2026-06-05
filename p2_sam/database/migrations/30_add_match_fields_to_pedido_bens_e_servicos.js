"use strict";

async function columnExists(queryInterface, table, column) {
  const [[{ cnt }]] = await queryInterface.sequelize.query(`
    SELECT COUNT(*) as cnt
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME = :table
      AND COLUMN_NAME = :column
  `, { replacements: { table, column } });
  return cnt > 0;
}

module.exports = {
  async up(queryInterface, Sequelize) {
    const table = "pedido_bens_e_servicos";

    if (!await columnExists(queryInterface, table, "match_negocio_nif")) {
      await queryInterface.addColumn(table, "match_negocio_nif", {
        type: Sequelize.STRING(9),
        allowNull: true,
        defaultValue: null,
      });
    }

    if (!await columnExists(queryInterface, table, "match_negocio_nome")) {
      await queryInterface.addColumn(table, "match_negocio_nome", {
        type: Sequelize.STRING(150),
        allowNull: true,
        defaultValue: null,
      });
    }

    if (!await columnExists(queryInterface, table, "match_negocio_estado")) {
      await queryInterface.addColumn(table, "match_negocio_estado", {
        type: Sequelize.ENUM("PENDENTE", "ACEITE", "RECUSADO", "CONCLUIDO"),
        allowNull: true,
        defaultValue: null,
      });
    }

    if (!await columnExists(queryInterface, table, "match_negocio_motivo")) {
      await queryInterface.addColumn(table, "match_negocio_motivo", {
        type: Sequelize.STRING(255),
        allowNull: true,
        defaultValue: null,
      });
    }
  },

  async down(queryInterface) {
    const table = "pedido_bens_e_servicos";
    await queryInterface.removeColumn(table, "match_negocio_motivo");
    await queryInterface.removeColumn(table, "match_negocio_estado");
    await queryInterface.removeColumn(table, "match_negocio_nome");
    await queryInterface.removeColumn(table, "match_negocio_nif");
  },
};
