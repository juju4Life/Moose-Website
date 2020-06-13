
function validateForm(formId, InputId, fieldError) {
  var x = document.forms[formId][InputId].value;
  if (x == "") {
    alert(fieldError);
    return false;
  }
}