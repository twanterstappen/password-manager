function delete_flash(flash){
    $(flash).parent().remove()
}

setTimeout(function() {
  $('.flash').fadeOut('slow', function() {
    $(this).remove();
  });
}, 5500);
