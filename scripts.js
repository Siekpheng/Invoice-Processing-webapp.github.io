// Handle Browse Button Click
document.getElementById('upload-btn').addEventListener('click', function () {
    document.getElementById('fileInput').click();
});

// Handle File Selection from Browse Button
document.getElementById('fileInput').addEventListener('change', function (e) {
    handleFiles(e.target.files);
});

// Handle Drag and Drop
const dragDropArea = document.getElementById('drag-drop-area');
dragDropArea.addEventListener('dragover', function (e) {
    e.preventDefault();
    dragDropArea.style.borderColor = '#007BFF'; // Highlight on drag
});

dragDropArea.addEventListener('dragleave', function (e) {
    dragDropArea.style.borderColor = '#ccc'; // Revert border
});

dragDropArea.addEventListener('drop', function (e) {
    e.preventDefault();
    dragDropArea.style.borderColor = '#ccc'; // Revert border after drop
    handleFiles(e.dataTransfer.files);
});

// Function to handle files
function handleFiles(files) {
    const fileList = document.getElementById('file-list');
    fileList.innerHTML = ''; // Clear any previous file list

    for (const file of files) {
        const listItem = document.createElement('div');
        listItem.textContent = file.name;
        fileList.appendChild(listItem);
    }
}
