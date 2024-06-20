$(document).ready(function () {
    let dialog = $('#dialog')

    dialog.dialog({autoOpen: false, modal: true});

    $('.activate-dialog').on('click', function () {
        dialog.dialog('open');
    })
})
