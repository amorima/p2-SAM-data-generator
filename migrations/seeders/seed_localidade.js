"use strict";

const path = require("path");
const data = require(path.join(__dirname, "../../output/localidade.json"));

module.exports = {
 async up(queryInterface) {
  const rows = data.map((r) => ({
   codigo_postal: r.codigo_postal,
   concelho: r.concelho ?? "Desconhecido",
   pais: r.pais ?? "Portugal",
   rua: (r.rua ?? "Rua Desconhecida").substring(0, 200),
   n_porta: r.n_porta ?? "S/N",
  }));

  await queryInterface.bulkInsert("localidade", rows, {
   ignoreDuplicates: true,
  });
 },

 async down(queryInterface) {
  await queryInterface.bulkDelete("localidade", null, {});
 },
};
