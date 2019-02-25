<<<<<<< HEAD
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

=======
(function (){
  var video = document.getElementById('video'),
      canvas = document.getElementById('canvas'),
      context = canvas.getContext('2d'),
      photo = document.getElementById('photo'),
      vendorUrl = window.URL || window.webkitURL;
  navigator.getMedia = navigator.getUserMedia ||
                       navigator.webkitGetUserMedia ||
                       navigator.mozGetUserMedia ||
                       navigator.msGetUserMedia;
                       
  navigator.getMedia({
    video: true,
    audio: false
  }, function(stream){
    video.srcObject=stream;
    video.play();
  }, function(error){
    //An error occured
    //error.code
  });

  document.getElementById('capture').addEventListener('click', function() {
    context.drawImage(video, 0, 0, 400, 300);
    photo.setAttribute('src', canvas.toDataURL('image/png'));
  });

>>>>>>> 3cae93abdfa9a0b1218d86a0bd0481a74a567511
})();