//source : https://developers.google.com/web/fundamentals/media/recording-audio


const downloadLink = document.getElementById('downloadButton');
const stopButton = document.getElementById('stopButton');
const startButton = document.getElementById('startButton');

const handleSuccess = function(stream) {
  const options = {mimeType: 'audio/webm'};
  const recordedChunks = [];
  const mediaRecorder = new MediaRecorder(stream, options);

  mediaRecorder.addEventListener('dataavailable', function(e) {
    // console.log("what?")
    if (e.data.size > 0) recordedChunks.push(e.data);
  });

  mediaRecorder.addEventListener('stop', function() {
    console.log('sending recorded sound')
    let data = new FormData();
    let blob =  new Blob(recordedChunks, {'type': 'audio/wav;'})
    // downloadLink.href = URL.createObjectURL(blob);
    // downloadLink.download = 'blob.wav';
    let reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = function () {
    let base64String = reader.result;
    
    data.append('sound', blob);
    console.log(blob);}
    // console.log(data.getAll('test'))






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
    ajaxRequest.open('POST', "http://localhost:5000/get_the_voice");
    // ajaxRequest.setRequestHeader("Content-type", "form-data");

    ajaxRequest.send(data);
    console.log('recorded data sent to server');















    //downloadLink.download = 'sound1.wav';
  });

  stopButton.addEventListener('click', function() {
    mediaRecorder.stop();
    console.log("recording stoped");
  });

  startButton.addEventListener('click', function() {
    mediaRecorder.start();
    console.log("recording started");
  });

};

navigator.mediaDevices.getUserMedia({ audio: true, video: false })
    .then(handleSuccess);