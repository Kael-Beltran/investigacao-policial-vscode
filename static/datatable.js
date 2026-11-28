/* Ativa o DataTables em toda <table class="js-datatable">.
   Colunas que não devem ordenar/pesquisar (ex.: botões): <th class="no-sort">. */
document.addEventListener("DOMContentLoaded", function () {
  if (typeof DataTable === "undefined") return;

  document.querySelectorAll("table.js-datatable").forEach(function (tabela) {
    new DataTable(tabela, {
      order: [],                       // mantém a ordem vinda do banco
      pageLength: 10,
      lengthMenu: [10, 25, 50, 100],
      columnDefs: [{ targets: "no-sort", orderable: false, searchable: false }],
      language: {
        search: "Pesquisar:",
        searchPlaceholder: "Digite para filtrar…",
        lengthMenu: "Mostrar _MENU_ registros",
        info: "Mostrando _START_ a _END_ de _TOTAL_ registros",
        infoEmpty: "Nenhum registro para mostrar",
        infoFiltered: "(filtrado de _MAX_ no total)",
        zeroRecords: "Nenhum registro encontrado para essa pesquisa",
        emptyTable: "Nenhum registro disponível",
        paginate: { first: "«", previous: "‹", next: "›", last: "»" }
      }
    });
  });
});
