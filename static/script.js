let mediaRecorder;
let chunks = [];

const btnStart = document.getElementById("start");
btnStart.addEventListener('click', async function() {
  btnStart.disabled = true;
  const stream = await navigator.mediaDevices.getUserMedia({
    video: false,
    audio: true
  });

  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.ondataavailable = (e) => chunks.push(e.data);

  mediaRecorder.onstop = async () => {
    const trs = document.getElementById("trs");
    trs.innerText = 'Analizing...';
    const blob = new Blob(chunks, { type: "audio/ogg" });
    
    // For Debug.
    const audio = document.getElementById("audio");
    const audioURL = window.URL.createObjectURL(blob);
    audio.src = audioURL;
    
    // Send To API.
    const fd = new FormData();
    fd.append('audio', blob, 'audio.ogg');
    const response = await fetch('http://localhost:5000/transcription', {
      method: 'post',
      body: fd,
    });
    const data = await response.text();
    trs.innerText = data;
    
    // Closing
    chunks = [];
    btnStart.disabled = false;
  }

  mediaRecorder.start();
});

const btnStop = document.getElementById("stop");
btnStop.addEventListener('click', function() {
  mediaRecorder.stop();
});
