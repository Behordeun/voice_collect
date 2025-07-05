let mediaRecorder;
let audioChunks = [];
let currentSentenceIndex = 0;

async function login() {
  const participant_id = document.getElementById('participant_id').value.trim();
  const email = document.getElementById('email').value.trim();

  if (!participant_id || !email) {
    alert("Please fill in both Participant ID and Email.");
    return;
  }

  const form = new FormData();
  form.append('participant_id', participant_id);
  form.append('email', email);

  try {
    await fetch('/login', {
      method: 'POST',
      body: form
    });
    alert('Login successful');
  } catch (error) {
    alert('Login failed');
    console.error(error);
  }
}

async function fetchSentence() {
  const participant_id = document.getElementById('participant_id').value.trim();
  if (!participant_id) {
    alert("Enter Participant ID first.");
    return;
  }

  try {
    const response = await fetch(`/sentence?participant_id=${participant_id}`);
    const data = await response.json();

    if (data.sentence) {
      document.getElementById('sentence').innerText = data.sentence;
      currentSentenceIndex = data.index;
    } else {
      document.getElementById('sentence').innerText = "All sentences completed.";
    }
  } catch (error) {
    alert("Failed to fetch sentence.");
    console.error(error);
  }
}

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
      if (event.data.size > 0) {
        audioChunks.push(event.data);
      }
    };

    mediaRecorder.start();
    alert("Recording started...");
  } catch (error) {
    alert("Microphone access denied or unavailable.");
    console.error(error);
  }
}

async function stopRecording() {
  if (!mediaRecorder) {
    alert("No recording in progress.");
    return;
  }

  mediaRecorder.stop();

  mediaRecorder.onstop = async () => {
    const blob = new Blob(audioChunks, { type: 'audio/wav' });

    const form = new FormData();
    form.append('file', blob, 'recording.wav');
    form.append('participant_id', document.getElementById('participant_id').value.trim());
    form.append('email', document.getElementById('email').value.trim());
    form.append('sentence_index', currentSentenceIndex);

    try {
      await fetch('/upload_audio', {
        method: 'POST',
        body: form
      });

      alert("Recording uploaded successfully.");
      fetchSentence();
    } catch (error) {
      alert("Failed to upload recording.");
      console.error(error);
    }
  };
}
