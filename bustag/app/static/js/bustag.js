$(function () {
    $('.coverimg').on('click', function () {
        $('#imglarge').attr('src', $(this).attr('src'));
        $('#imagemodal').modal('show');
    });

    $('#pagenav').on('change', function () {
        window.location = $(this).val();
    });
});