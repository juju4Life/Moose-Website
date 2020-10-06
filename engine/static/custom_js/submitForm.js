

$('#submit').click(function(url, method, data) {
    $.ajax({
        url: url,
        type: method,
        data: data,
        success: function(msg) {
            alert('Email Sent');
        }
    });
});

function submitForm(event) {
    this.preventDefault()
}