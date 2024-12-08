django.jQuery(document).ready(function () {
    const csrftoken = Cookies.get('csrftoken');

    function addError(modalContent, error) {
        modalContent.addClass('errors');
        const list = modalContent.prepend('<ul class="errorlist"></ul>').find('ul');
        list.append(`<li>${error}</li>`);
    }

    function removeError(modalContent) {
        modalContent.removeClass('errors');
        modalContent.find('.errorlist').remove();
    }

    django.jQuery('.successConfirm').on('click', function () {
        const button = django.jQuery(this);
        const data = button.data();

        const modal = button.closest('.modal');
        const modalContent = modal.find('.modal-content');

        removeError(modalContent);

        django.jQuery.ajax({
            url: data['actionUrl'],
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            error: function (response) {
                const error = response.responseJSON['error'];
                addError(modalContent, error);
            },
            success: function (data) {
                window.location.replace(data['redirectUrl']);
            },
        })
    })
})