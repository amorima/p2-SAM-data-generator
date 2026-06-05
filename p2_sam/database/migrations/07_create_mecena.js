"use strict";

// Mecena era uma tabela intermédia IS-A sem colunas de dados.
// Após normalização, o papel de mecenas é identificado por entidade.role = 'patron'.
// Esta migration é mantida por compatibilidade de sequência mas não cria tabela.
module.exports = {
 async up() {},
 async down() {},
};
