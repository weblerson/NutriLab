function downloadFile(href, file) {
  let a = document.createElement("a");
  a.style.display = "none";
  a.href = href;
  a.download = file;
  a.target = "_blank";
  document.body.appendChild(a);
  a.click();

  console.log("Downloaded");
}

function sendMarkup() {
  let plano = document.querySelector("#plano-alimentar").outerHTML;
  let btn = document.querySelector("#export");

  let nomePaciente = btn.name;

  let data = {
    html: plano,
    name: nomePaciente,
  };

  fetch("http://127.0.0.1:8000/api/plano_alimentar", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  })
    .then((response) => response.json())
    .then((response) => {
      if (response.success) {
        downloadFile(response.body, `${data.name}.pdf`);
      } else {
        console.log("fudeu");
      }
    });
}
