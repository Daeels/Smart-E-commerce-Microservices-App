//source : https://developers.google.com/web/fundamentals/media/recording-audio


const downloadLink = document.getElementById('downloadButton');
  const stopButton = document.getElementById('stopButton');
  const startButton = document.getElementById('startButton');

  const handleSuccess = function(stream) {
    const options = {mimeType: 'audio/webm'};
    const recordedChunks = [];
    const mediaRecorder = new MediaRecorder(stream, options);

    mediaRecorder.addEventListener('dataavailable', function(e) {
      console.log("what?")
      if (e.data.size > 0) recordedChunks.push(e.data);
    });

    mediaRecorder.addEventListener('stop', function() {
      console.log('stopped recording?')
      downloadLink.href = URL.createObjectURL(new Blob(recordedChunks));
      let data = new FormData();
      data.append('sound', new Blob(recordedChunks));
      data.append('test', 'test');
      console.log(data.getAll('test'))




      let ajaxRequest = new XMLHttpRequest();
      ajaxRequest.onreadystatechange = function(){
        if(ajaxRequest.readyState == 4){
          if (ajaxRequest.status == 200){
            console.log(ajaxRequest.responseText)
          }
        else if(ajaxRequest.status == 0){
          alert("Aucune réponse du serveur");
        }
        else{
          alert(ajaxRequest.responseText);

        }
      
        }
      }
      ajaxRequest.open('POST', "http://localhost:5001/client");
      // ajaxRequest.setRequestHeader("Content-type", "application/json");
      ajaxRequest.send(data);















      //downloadLink.download = 'sound1.wav';
    });

    stopButton.addEventListener('click', function() {
      mediaRecorder.stop();
    });

    startButton.addEventListener('click', function() {
      mediaRecorder.start();
    });

  };

  navigator.mediaDevices.getUserMedia({ audio: true, video: false })
      .then(handleSuccess);