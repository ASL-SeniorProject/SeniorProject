var counter = 0;

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

function testCal(){
	if (counter > 20){
		console.log("exiting");
		return;
	}
	counter += 1;
	context.drawImage(video, 0, 0, 352, 228);
	photo.setAttribute('src', canvas.toDataURL('image/jpg'));
	var data = canvas.toDataURL('image/jpg');

	data = data.substring(22, data.length);
	var xhttp = new XMLHttpRequest();
	var url = "http://localhost:5000/calibrate/";

	var theUrl = "http://localhost:5000/addLetter/ Ok";
	
	var data = {"image":data};
	complete = false;
	$.ajax({
		type: 'POST',
		async:false,
		contentType: 'application/json',
		url: 'http:localhost:5000/calibrate',
		dataType : 'json',
		data : JSON.stringify(data),
		success : function(result) {
		  console.log("recursing");
		  testCal();
		  console.log("recursed");
		  //jQuery("#clash").html(result);
		},error : function(result){
		   console.log("error");
		   console.log(result);
		}
	});
}

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
    photo.setAttribute('src', canvas.toDataURL('image/jpg'));
    var data = canvas.toDataURL('image/jpg')

    data = data.substring(22, data.length)
    var xhttp = new XMLHttpRequest();
    var url = "http://localhost:5000/processImage/"

    var theUrl = "http://localhost:5000/addLetter/ Ok"

    
    var data = {"image":data}
	$.ajax({
		type: 'POST',
		contentType: 'application/json',
		url: 'http:localhost:5000/processImage',
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


(function (){  
  document.getElementById('calibrate').addEventListener('click', function() {
	testCal();
  });
  document.getElementById('predict').addEventListener('click', function() {
	var data = "boogers";
	$.ajax({
		type: 'GET',
		contentType: 'application/json',
		url: 'http:localhost:5000/predict',
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

