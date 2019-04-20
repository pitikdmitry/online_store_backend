(function () {
  let fileCatcher = document.getElementById('file-catcher-id');
  let fileInput = document.getElementById('file-input');
  let fileListDisplay = document.getElementById('file-list-display');

  let fileList = [];
  let renderFileList, sendFile;
  let form = document.forms.namedItem("file-catcher");


  fileCatcher.addEventListener('submit', function (evnt) {
    evnt.preventDefault();

    sendFile(fileList);

    //
    // fileList.forEach(function (file) {
    // });
  });

  fileInput.addEventListener('change', function (evnt) {
    fileList = [];
    for (let i = 0; i < fileInput.files.length; i++) {
      fileList.push(fileInput.files[i]);
    }
    renderFileList();
  });

  renderFileList = function () {
    fileListDisplay.innerHTML = '';
    fileList.forEach(function (file, index) {
      let fileDisplayEl = document.createElement('p');
      fileDisplayEl.innerHTML = (index + 1) + ': ' + file.name;
      fileListDisplay.appendChild(fileDisplayEl);
    });
  };

  sendFile = function (fileList) {
    // let form = document.getElementById("file-catcher");

    let formData = new FormData(form);
    for (var [key, value] of formData.entries()) {
      console.log(key, value);
    }
    let request = new XMLHttpRequest();

    debugger;
    formData.set('file', fileList[0]);
    request.open("POST", 'http://localhost:8080/api/post/add');
    request.send(formData);
  };
})();
