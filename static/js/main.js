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
      var xhr = new XMLHttpRequest();
      xhr.onreadystatechange = function() {
    switch ( xhr.readyState ) {
        case 0:
            // 未初期化状態.
            console.log( 'uninitialized!' );
            break;
        case 1: // データ送信中.
            console.log( 'loading...' );
            break;
        case 2: // 応答待ち.
            console.log( 'loaded.' );
            break;
        case 3: // データ受信中.
            console.log( 'interactive... '+xhr.responseText.length+' bytes.' );
            break;
        case 4: // データ受信完了.
            if( xhr.status == 200 || xhr.status == 304 ) {
                var data = xhr.responseText; // responseXML もあり
                console.log( 'COMPLETE! :'+data );
            } else {
                console.log( 'Failed. HttpStatus: '+xhr.statusText );
            }
            break;
    }
};
      xhr.open('POST', data.url, true)
      xhr.send(fd);
    })
    $(this).val('');
  });
});

