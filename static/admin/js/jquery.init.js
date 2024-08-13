// override js file django/contrib/admin/static/admin/js/jquery.init.js

window.django = {jQuery: jQuery.noConflict(true)};
window.jQuery = window.$ = django.jQuery;
