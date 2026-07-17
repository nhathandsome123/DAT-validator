const form = document.getElementById('upload-form');
const statusBox = document.getElementById('status');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  statusBox.className = 'card';
  statusBox.innerHTML = '<p>Processing…</p>';
  const button = form.querySelector('button');
  button.disabled = true;

  const formData = new FormData(form);
  try {
    const response = await fetch('/process', { method: 'POST', body: formData });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Processing failed');

    statusBox.classList.add(data.error_count > 0 ? 'error' : data.warning_count > 0 ? 'warning' : 'success');
    statusBox.innerHTML = `
      <h2>Done</h2>
      <ul>
        <li>Total sessions: <strong>${data.total_sessions}</strong></li>
        <li>Errors: <strong>${data.error_count}</strong></li>
        <li>Warnings: <strong>${data.warning_count}</strong></li>
        <li>Processing time: <strong>${data.elapsed_seconds}s</strong></li>
      </ul>
      <p><a href="${data.download_url}">Download report</a></p>
    `;
  } catch (error) {
    statusBox.classList.add('error');
    statusBox.innerHTML = `<h2>Failed</h2><p>${error.message}</p>`;
  } finally {
    button.disabled = false;
    statusBox.classList.remove('hidden');
  }
});
