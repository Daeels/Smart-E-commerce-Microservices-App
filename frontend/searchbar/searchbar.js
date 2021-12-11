//https://stackoverflow.com/questions/40729039/pcm-support-in-webm-and-chromes-webm-implementation
//https://stackoverflow.com/questions/51368252/setting-blob-mime-type-to-wav-still-results-in-webm


const stopButton = document.getElementById('stopButton');
const startButton = document.getElementById('startButton');

const handleSuccess = function(stream) {
  const options = {mimeType: 'audio/webm'}; //'auido/wav' is not supported
  const recordedChunks = [];
  const mediaRecorder = new MediaRecorder(stream, options);

  mediaRecorder.addEventListener('dataavailable', function(e) {
    console.log("audio data is being recorded")
    if (e.data.size > 0) recordedChunks.push(e.data);
  });


  mediaRecorder.addEventListener('stop', function() {
    console.log('stopped recording');
    let data = {};
    let blob = new Blob(recordedChunks);
    let reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = function () {
      let base64String = reader.result;
      let base64StringRaw = base64String.substr(base64String.indexOf(',') + 1);
      // console.log(base64StringRaw)
      data['sound'] = base64StringRaw;
        


      let ajaxRequest = new XMLHttpRequest();
          ajaxRequest.onreadystatechange = function(){
            if(ajaxRequest.readyState == 4){
              if (ajaxRequest.status == 200){
                console.log(ajaxRequest.responseText);
              }
            else if(ajaxRequest.status == 0){
              alert("Aucune réponse du serveur");
            }
            else{
              alert(ajaxRequest.responseText);

            }
          
            }
          }
      ajaxRequest.open('POST', "http://localhost:5000/search-by-voice");
      ajaxRequest.setRequestHeader("Content-Type", "application/json");
      data = JSON.stringify(data);
      ajaxRequest.send(data);
      // console.log(data);
      
      }


    });


    stopButton.addEventListener('click', function() {
      try {
        mediaRecorder.stop();
      }
      catch(e) {
        if (e.name == "InvalidStateError") {
            alert('Please start record first');
        }
      }
    });


    startButton.addEventListener('click', function() {
      //Empty the recorder before recording anything new
      recordedChunks.length = 0; 
      //Start recording
      try{
        mediaRecorder.start();
        console.log('started recording')
      }
      catch(e) {
        if (e.name == "InvalidStateError") {
            alert('already recording');
        }
        
      }
    });

  };


navigator.mediaDevices.getUserMedia({ audio: true, video: false })
    .then(handleSuccess);


    //http://localhost:8443/products/search/productsByKeyword?mc=zikas