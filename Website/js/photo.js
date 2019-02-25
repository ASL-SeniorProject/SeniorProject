(function (){
  var video = document.getElementById('photo');
  var vendorURL = window.URL || window.webkitURL;
  var canvas = document.getElementById('canvas');
  var context = canvas.getContext('2d');
  var photo = document.getElementById('photo')
  navigator.getMedia = navigator.getUserMedia ||
                       navigator.webkitGetUserMedia ||
                       navigator.mozGetUserMedia ||
                       navigator.msGetUserMedia;
  navigator.getMedia({
    video: true,
    audio: false
  }, function(stream){
    video.src = vendorURL.createObjectURL(stream);
    video.play();
  }, function(error){
    //An error occured
    //error.code
  });

  document.getElementById('capture').addEventListener('click', function() {
    context.drawImage(video, 0, 0, 400, 300);
    photo.setAttribute('src', canvas.toDataURL('image/png'));
  });

})();