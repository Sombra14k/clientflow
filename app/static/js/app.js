// Filtro instantâneo de tabelas (campo com data-filter="#idDaTabela")
document.querySelectorAll("[data-filter]").forEach(function (input) {
  var rows = document.querySelectorAll(input.dataset.filter + " tbody tr");
  input.addEventListener("input", function () {
    var term = input.value.toLowerCase();
    rows.forEach(function (tr) {
      tr.hidden = term && !tr.textContent.toLowerCase().includes(term);
    });
  });
});

// Confirmação antes de excluir
document.querySelectorAll("form[data-confirm]").forEach(function (form) {
  form.addEventListener("submit", function (e) {
    if (!window.confirm(form.dataset.confirm)) e.preventDefault();
  });
});
