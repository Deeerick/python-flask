// Toast:
$(document).ready(function () {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function (toastEl) {
      return new bootstrap.Toast(toastEl, {
        delay: 3000
      });
    });
    toastList.forEach(toast => toast.show());
  });
