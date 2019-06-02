function UpdateText() {
    var text = "Hello"
    console.log(text)
    function update() {
        $.ajax({
            url: "http:localhost:5000/",
            type: 'GET',
            
            success: function(res) {
                console.log(res)
                document.getElementById("myTextarea").value = res;
                
            
            }
        });
      
    }
    setInterval(update, 10000);
    
    update();
}

window.onload = UpdateText();