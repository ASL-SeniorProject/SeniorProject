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
    context.drawImage(video, 0, 0, 352, 228);
    photo.setAttribute('src', canvas.toDataURL('image/png'));
    var data = canvas.toDataURL('image/png')

    data = data.substring(22, data.length)
    var xhttp = new XMLHttpRequest();
    var url = "http://localhost:5010/processImage/"

    var theUrl = "http://68.80.81.129:5010/addLetter/ Ok"

    
    var data = {"image":data}
$.ajax({
    type: 'POST',
    contentType: 'application/json',
    url: 'http:68.80.81.129:5010/processImage',
    dataType : 'json',
    data : JSON.stringify(data),
    success : function(result) {
      jQuery("#clash").html(result); 
    },error : function(result){
       console.log(result);
    }
});
    
  });
  
})();