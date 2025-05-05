interface Preferences {
  sceneAgent: boolean;
  colorAgent: boolean;
  outputMP4: boolean;
  outputGIF: boolean;
  outputPNG: boolean;
}

function savePreferences(): void {
  const preferences: Preferences = {
    sceneAgent: (document.getElementById('scene-agent') as HTMLInputElement)?.checked,
    colorAgent: (document.getElementById('color-agent') as HTMLInputElement)?.checked,
    outputMP4: (document.getElementById('output-mp4') as HTMLInputElement)?.checked,
    outputGIF: (document.getElementById('output-gif') as HTMLInputElement)?.checked,
    outputPNG: (document.getElementById('output-png') as HTMLInputElement)?.checked,
  };

  localStorage.setItem('aiToSvgPreferences', JSON.stringify(preferences));
}

function loadPreferences(): void {
  const raw = localStorage.getItem('aiToSvgPreferences');
  if (!raw) return;

  try {
    const preferences: Preferences = JSON.parse(raw);
    (document.getElementById('scene-agent') as HTMLInputElement).checked = preferences.sceneAgent;
    (document.getElementById('color-agent') as HTMLInputElement).checked = preferences.colorAgent;
    (document.getElementById('output-mp4') as HTMLInputElement).checked = preferences.outputMP4;
    (document.getElementById('output-gif') as HTMLInputElement).checked = preferences.outputGIF;
    (document.getElementById('output-png') as HTMLInputElement).checked = preferences.outputPNG;
  } catch (err) {
    console.error("Failed to load preferences:", err);
  }
}

function validateFile(): void {
  const input = document.getElementById('config-file') as HTMLInputElement;
  const errorElement = document.getElementById('file-error') as HTMLElement;

  input.addEventListener('change', (e: Event) => {
    const file = (e.target as HTMLInputElement).files?.[0];

    if (!file) return;

    if (file.type !== 'application/json') {
      errorElement.textContent = 'Invalid file type. Please upload a JSON file.';
      input.value = '';
    } else if (file.size > 5 * 1024 * 1024) {
      errorElement.textContent = 'File size exceeds 5MB. Please upload a smaller file.';
      input.value = '';
    } else {
      errorElement.textContent = '';
    }
  });
}

function setupPipelineRunner(): void {
  const runButton = document.getElementById('run-pipeline') as HTMLButtonElement;
  const progressBar = document.getElementById('progress') as HTMLElement;
  const status = document.getElementById('status') as HTMLElement;

  runButton.addEventListener('click', () => {
    savePreferences();
    status.textContent = 'Running pipeline...';
    progressBar.style.width = '50%';

    setTimeout(() => {
      progressBar.style.width = '100%';
      status.textContent = '✅ Pipeline completed successfully!';
    }, 2000);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  loadPreferences();
  validateFile();
  setupPipelineRunner();
});
