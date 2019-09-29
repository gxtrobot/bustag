$(function () {
    $('.coverimg').on('click', function () {
        $('#imglarge').attr('src', $(this).attr('src'));
        $('#imagemodal').modal('show');
    });
});