const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const progressBar = document.getElementById("progress");
const status = document.getElementById("status");

dropzone.onclick = () => fileInput.click();

dropzone.addEventListener("dragover", e => {
  e.preventDefault();
  dropzone.classList.add("dragover");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("dragover");
});

dropzone.addEventListener("drop", e => {
  e.preventDefault();
  dropzone.classList.remove("dragover");
  upload(e.dataTransfer.files);
});

fileInput.onchange = () => upload(fileInput.files);

function upload(files) {
  if (!files || files.length === 0) return;

  let form = new FormData();
  for (let f of files) form.append("files", f);

  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/", true);

  xhr.upload.onprogress = e => {
    if (e.lengthComputable) {
      let percent = (e.loaded / e.total) * 100;
      progressBar.value = percent;
      status.innerText = Math.round(percent) + "% uploaded";
    }
  };

  xhr.onload = () => {
    status.innerHTML = xhr.responseText;
    progressBar.value = 0;
  };

  xhr.send(form);
}
