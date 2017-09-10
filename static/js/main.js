$(function() {
  $('#inputFile').change(function (e){
    var file = e.target.files[0];
    console.log(file.name)
    $.ajax({
      url: '/owner/policies/',
      type: 'POST',
      dataType: 'json',
      data: {
        size: file.size,
        content_type: file.type
      }
    }).done(function (data) {
      var name, fd = new FormData();
      for (name in data.form) if (data.form.hasOwnProperty(name)) {
        fd.append(name, data.form[name]);
        console.log(name + ":" + data.form[name]);
      }
      fd.append('file', file);
    })
    $(this).val('');
  });
});

