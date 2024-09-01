const transmissionDropdown = document.getElementById('dropdown');
const fuelDropdown = document.getElementById('fuelDropdown');
const projectname = document.getElementById('projectname');
const username = document.getElementById('username');
const idElement = document.getElementById('id');
const circumferenceElement = document.getElementById('circumference');


function openModal(buttonId) {
  var modal = document.getElementById("ModalDirec");
  var titleElement = document.getElementById("modalTitle");
  if (titleElement) {
    switch (buttonId) {
      case "aceleration":
        titleElement.textContent = "Aceleration Metrics";
        break;
      case "coastdown":
        titleElement.textContent = "Coast Down";
        break;
      case "wot":
        titleElement.textContent = "Full load (WOT)";
        break;
      case "parasitic":
        titleElement.textContent = "Parasitic Losses";
        break;
      case "rr":
        titleElement.textContent = "Rolling Resistance";
        break;
      default:
        closeModal();
        return;
    }
  }

  modal.style.display = "block";
}


function closeModal() {
  var modal = document.getElementById("ModalDirec");
  modal.style.display = "none";
}

var buttons = document.querySelectorAll(".dropbtn");


buttons.forEach(function (button) {
  button.addEventListener("click", function () {
    var buttonId = this.id; 
    openModal(buttonId);
  });
});


function handleTransmissionSelection() {
  const selectedOption = transmissionDropdown.value;

  
  console.log("Transmission selecionado:", selectedOption);
}


function handleFuelSelection() {
  const selectedOption = fuelDropdown.value;

  
  console.log("Fuel selecionado:", selectedOption);
}


transmissionDropdown.addEventListener('change', handleTransmissionSelection);
fuelDropdown.addEventListener('change', handleFuelSelection);

function enviarDados() {
  
  var transmission = transmissionDropdown.value;
  var fuelType = fuelDropdown.value;
  var projectName = projectname.value;
  var id = idElement.value;
  var userName = username.value;
  var circumference = circumferenceElement.value;
  var buttonId = document.getElementById('modalTitle').textContent;

  
  var dados = {
    transmission: transmission,
    fuelType: fuelType,
    circumference: circumference,
    projectname: projectName,
    id: id,
    username: userName,
    buttonId: buttonId
  };

  
  fetch('/processar_dados', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dados)
  })
    .then(response => response.json())
    .catch(error => {
      
      console.error('Ocorreu um erro:', error);
    });
}

function confirmModal() {
  
  closeModal(); 
  enviarDados(); 
}

function runPythonConvertertdms() {
  $.ajax({
    type: "POST",
    url: "/runPythonConvertertdms",
    success: function (response) {
      alert("Resultado do código Python: " + response);
    }
  });
  return false;
}

document.getElementById("tdms").addEventListener("click", runPythonConvertertdms);

function runPythonConverterdat() {
  $.ajax({
    type: "POST",
    url: "/runPythonConverterdat",
    success: function (response) {
      alert("Resultado do código Python: " + response);
    }
  });
}

document.getElementById("dat").addEventListener("click", runPythonConverterdat);

function runPythonConverterbin() {
  $.ajax({
    type: "POST",
    url: "/runPythonConverterbin",
    success: function (response) {
      alert("Resultado do código Python: " + response);
    }
  });
}

document.getElementById("bin").addEventListener("click", runPythonConverterbin);

function runPythonAnalysisWOT() {
  $.ajax({
    type: "POST",
    url: "/runPythonAnalysisWOT",
    success: function (response) {
      alert("Resultado do código Python: " + response);
    }
  });
}

document.getElementById("wot").addEventListener("click", runPythonAnalysisWOT);

function runPythonAnalysisAceleration() {
  $.ajax({
    type: "POST",
    url: "/runPythonAnalysisAceleration",
    success: function (response) {
      alert("Resultado do código Python: " + response);
    }
  });
}

document.getElementById("aceleration").addEventListener("click", runPythonAnalysisAceleration);

function runPythonAnalysisCoastdown() {
  $.ajax({
    type: "POST",
    url: "/runPythonAnalysisCoastdown",
    success: function (response) {
      alert("Resultado do código Python: " + response);
    }
  });
}

document.getElementById("coastdown").addEventListener("click", runPythonAnalysisCoastdown);

function runPythonAnalysisParasitic() {
  $.ajax({
    type: "POST",
    url: "/runPythonAnalysisParasitic",
    success: function (response) {
      alert("Resultado do código Python: " + response);
    }
  });
}

document.getElementById("parasitic").addEventListener("click", runPythonAnalysisParasitic);
