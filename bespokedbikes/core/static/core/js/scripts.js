setTimeout(function () {
  var errorAlert = document.querySelectorAll("#error-alert");
  for (let i = 0; i < errorAlert.length; i++) {
    if (errorAlert[i]) {
        errorAlert[i].style.display = "none";
      }
  }
}, 5000);
