// Save preferences to localStorage
function savePreferences() {
  const preferences = {
    sceneAgent: document.getElementById('scene-agent').checked,
    colorAgent: document.getElementById('color-agent').checked,
    outputMP4: document.getElementById('output-mp4').checked,
    outputGIF: document.getElementById('output-gif').checked,
    outputPNG: document.getElementById('output-png').checked
  };
  localStorage.setItem('aiToSvgPreferences', JSON.stringify(preferences));
}

// Load preferences from localStorage
function loadPreferences() {
  const preferences = JSON.parse(localStorage.getItem('aiToSvgPreferences'));
  if (preferences) {
    document.getElementById('scene-agent').checked = preferences.sceneAgent;
    document.getElementById('color-agent').checked = preferences.colorAgent;
    document.getElementById('output-mp4').checked = preferences.outputMP4;
    document.getElementById('output-gif').checked = preferences.outputGIF;
    document.getElementById('output-png').checked = preferences.outputPNG;
  }
}

// File validation
document.getElementById('config-file').addEventListener('change', (e) => {
  const file = e.target.files[0];
  const errorElement = document.getElementById('file-error');
  
  if (file && file.type !== 'application/json') {
    errorElement.textContent = 'Invalid file type. Please upload a JSON file.';
    e.target.value = ''; // Reset the input
  } else if (file && file.size > 5 * 1024 * 1024) {
    errorElement.textContent = 'File size exceeds 5MB. Please upload a smaller file.';
    e.target.value = '';
  } else {
    errorElement.textContent = '';
  }
});

// Run pipeline
document.getElementById('run-pipeline').addEventListener('click', async () => {
  const progressBar = document.getElementById('progress');
  const status = document.getElementById('status');
  
  // Save preferences
  savePreferences();
  
  // Simulate backend call
  status.textContent = 'Running pipeline...';
  progressBar.style.width = '50%';
  
  // Simulate delay
  setTimeout(() => {
    progressBar.style.width = '100%';
    status.textContent = '✅ Pipeline completed successfully!';
  }, 2000);
});

// Load preferences on startup
document.addEventListener('DOMContentLoaded', loadPreferences);