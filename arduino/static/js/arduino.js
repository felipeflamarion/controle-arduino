$(document).ready(function () {
    // ===== ESTILIZAR DROPDOWNS ===== //
    $('#id_local').dropdown();
    $('#id_categoria').dropdown();
    $('#id_tags').dropdown();
    $('#id_usuarios').dropdown();
});



$('.abrirModalConfirmacao').click(function () {
    $('.modalConfirmacao').modal('show');
});

