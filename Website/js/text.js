function UpdateText() {
    var text = "Hello"
    console.log(text)
    function update() {
        $.ajax({
            url: "http:68.80.81.129:5010/",
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