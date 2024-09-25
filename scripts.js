// Ensure 'Browse Files' button triggers file selection
document.getElementById('upload-btn').addEventListener('click', function () {
    document.getElementById('fileInput').click();  // Trigger file input click
});

// Handle file selection from the 'Browse Files' button
document.getElementById('fileInput').addEventListener('change', function (e) {
    displayFiles(e.target.files);  // Display selected files
});

// Handle drag and drop events
const dragDropArea = document.getElementById('drag-drop-area');
dragDropArea.addEventListener('dragover', function (e) {
    e.preventDefault();
    dragDropArea.style.borderColor = '#007BFF';  // Highlight area when dragging over
});

dragDropArea.addEventListener('dragleave', function () {
    dragDropArea.style.borderColor = '#ccc';  // Revert border on drag leave
});

dragDropArea.addEventListener('drop', function (e) {
    e.preventDefault();
    dragDropArea.style.borderColor = '#ccc';  // Revert border after drop
    displayFiles(e.dataTransfer.files);  // Display dropped files
});

// Function to display uploaded files with download links using FileReader
function displayFiles(files) {
    const fileList = document.getElementById('file-list');
    fileList.innerHTML = '';  // Clear any previous file list

    for (const file of files) {
        const listItem = document.createElement('div');
        listItem.textContent = file.name;

        const reader = new FileReader();
        reader.onload = function (e) {
            const downloadLink = document.createElement('a');
            downloadLink.href = e.target.result;
            downloadLink.download = file.name;
            downloadLink.textContent = ' Download';
            downloadLink.style.marginLeft = '10px';

            listItem.appendChild(downloadLink);
        };
        reader.readAsDataURL(file);  // Convert file to a base64-encoded URL

        fileList.appendChild(listItem);
    }
}
