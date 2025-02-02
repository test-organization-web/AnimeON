django.jQuery(document).ready(function () {
    const csrftoken = Cookies.get('csrftoken');

    function addError(modalContent, error) {
        modalContent.addClass('errors');
        const list = modalContent.prepend('<ul class="errorlist"></ul>').find('ul');
        list.append(`<li>This field is required.</li>`);
    }

    function removeError(modalContent) {
        modalContent.removeClass('errors');
        modalContent.find('.errorlist').remove();
    }

    django.jQuery('.addComment').on('click', function () {
        const button = django.jQuery(this);
        const data = button.data();

        const modal = button.closest('.modal');
        const inputField = modal.find('.userComment');
        const modalContent = modal.find('.modal-content');
        const inputValue = inputField.val();

        removeError(modalContent);

        django.jQuery.ajax({
            url: data['actionUrl'],
            method: 'POST',
            data: {
                'userComment': inputValue,
            },
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