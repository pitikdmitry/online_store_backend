(function () {
  let fileCatcher = document.getElementById('file-catcher-id');
  let fileInput = document.getElementById('file-input');
  let fileListDisplay = document.getElementById('file-list-display');

  let fileList = [];
  let renderFileList, sendFile, loadCategories;
  let form = document.forms.namedItem("file-catcher");
  let select = document.getElementById("category-select");

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

  loadCategories = function () {
    fetch('http://localhost:8080/api/category/get_all', {
            mode: 'cors',
            headers: {
                'Access-Control-Allow-Origin': '*'
            }
        }).then(res => res.json())
        .then(function (response) {
            let categorySelect = document.getElementById("category-select");
            response.forEach(function myFunction(value, index, array) {

                let option = document.createElement("option");
                option.text = value.title;
                categorySelect.add(option);
            });
        })
    };

  loadCategories();


  sendFile = function (fileList) {
    let formData = new FormData(form);
    for (let [key, value] of formData.entries()) {
      console.log(key, value);
    }
    let request = new XMLHttpRequest();
    // let category = select.options[select.selectedIndex].value;

    formData.set('file', fileList[0]);
    request.open("POST", 'http://localhost:8080/api/post/add');
    request.send(formData);
  };
})();
