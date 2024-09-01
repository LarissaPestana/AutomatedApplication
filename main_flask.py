import json
import subprocess
import webview

from flask import Flask, jsonify , render_template, request

app= Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/converter')
def converter():

    return render_template('converter.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/directory')
def directory():
    return render_template('directory.html')
    
html = """
    <style>
        body {
            background-color: #333;
            color: white;
            font-family: Helvetica Neue, Helvetica, Arial, sans-serif;
        }

        .main-container {
            width: 100%;
            height: 90vh;
            display: flex;
            display: -webkit-flex;
            align-items: center;
            -webkit-align-items: center;
            justify-content: center;
            -webkit-justify-content: center;
            overflow: hidden;
        }

        .loading-container {
        }

        .loader {
          font-size: 10px;
          margin: 50px auto;
          text-indent: -9999em;
          width: 3rem;
          height: 3rem;
          border-radius: 50%;
          background: #ffffff;
          background: -moz-linear-gradient(left, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
          background: -webkit-linear-gradient(left, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
          background: -o-linear-gradient(left, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
          background: -ms-linear-gradient(left, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
          background: linear-gradient(to right, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
          position: relative;
          -webkit-animation: load3 1.4s infinite linear;
          animation: load3 1.4s infinite linear;
          -webkit-transform: translateZ(0);
          -ms-transform: translateZ(0);
          transform: translateZ(0);
        }
        .loader:before {
          width: 50%;
          height: 50%;
          background: #ffffff;
          border-radius: 100% 0 0 0;
          position: absolute;
          top: 0;
          left: 0;
          content: '';
        }
        .loader:after {
          background: #333;
          width: 75%;
          height: 75%;
          border-radius: 50%;
          content: '';
          margin: auto;
          position: absolute;
          top: 0;
          left: 0;
          bottom: 0;
          right: 0;
        }
        @-webkit-keyframes load3 {
          0% {
            -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
          }
          100% {
            -webkit-transform: rotate(360deg);
            transform: rotate(360deg);
          }
        }
        @keyframes load3 {
          0% {
            -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
          }
          100% {
            -webkit-transform: rotate(360deg);
            transform: rotate(360deg);
          }
        }

        .loaded-container {
            display: none;
        }


    </style>
    <body>
        <div class="main-container">
            <div id="loader" class="loading-container">
                <div class="loader">Loading...</div>
            </div>

            <div id="main" class="loaded-container">
                <img src="{{ url_for('static', filename='images/logo1.png') }}" />
                
            </div>
        </div>

      <script>
          setTimeout(function() {
              document.getElementById('loader').style.display = 'none'
              document.getElementById('main').style.display = 'block'
          }, 5000)
      </script>
    </body>
"""

def processar_dados(dados):
    resultados = {
        'message': 'Dados recebidos e processados com sucesso.',
        'dados_processados': dados
    }

    return resultados


@app.route('/processar_dados', methods=['POST'])
def processar_dados_route():
    dados = request.get_json()


    with open('dados.json', 'w') as arquivo:
        json.dump(dados, arquivo)
        
    
    button_id = dados.get('buttonId')
    if button_id == 'Aceleration Metrics':
        subprocess.run(['python', 'directoryacceleration.py'])
        result = 'Aceleration Metrics executed'
    elif button_id == 'Coast Down':
        subprocess.run(['python', 'directorycoastdown.py'])
        result = 'Coast Down executed'
    elif button_id == 'Full load (WOT)':
        subprocess.run(['python', 'directorywot.py'])
        result = 'Full load (WOT) executed'
    elif button_id == 'Parasitic Losses':
        subprocess.run(['python', 'directoryparasitic.py'])
        result = 'Parasitic Losses executed'
    else:
        result = 'No script executed'
   



@app.route('/runPythonConvertertdms', methods=['POST'])
def execute_python_code_tdms():
    
    subprocess.run(['python', 'code_convertertdms.py'], check=True)
    return '', 204

@app.route('/runPythonConverterdat', methods=['POST'])
def execute_python_code_dat():
    
    subprocess.run(['python', 'testedat.py'],check=True)
    return '', 204

@app.route('/runPythonConverterbin', methods=['POST'])
def execute_python_code_bin():
    
    subprocess.run(['python', 'code_converterbin.py'],check=True)
    return '', 204
    

@app.route('/runPythonAnalysisWOT', methods=['POST'])
def execute_python_analysis_wot():
    subprocess.run(['python', 'runWOT.py'], check=True)
    return jsonify({'message': 'Análise Python concluída.'})

@app.route('/runPythonAnalysisAceleration', methods=['POST'])
def execute_python_analysis_acc():
    subprocess.run(['python', 'runacc.py'], check=True)
    return jsonify({'message': 'Análise Python concluída.'})

@app.route('/runPythonAnalysisCoastdown', methods=['POST'])
def execute_python_analysis_cdb():
    subprocess.run(['python', 'runcoastdown.py'], check=True)
    return jsonify({'message': 'Análise Python concluída.'})


@app.route('/runPythonAnalysisParasitic', methods=['POST'])
def execute_python_analysis_parasitic():
    subprocess.run(['python', 'runparasiticlosses.py'], check=True)
    return jsonify({'message': 'Análise Python concluída.'})

if __name__ == '__main__':
     window = webview.create_window("Integrated System - EMAT", url= app, width=1900, height=1900,)
     #webview.start()
     #app.run(port=8080, host='0.0.0.0', debug=True, threaded=True)
     
    


