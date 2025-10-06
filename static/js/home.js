
// import * as echarts from 'echarts';


function renderBarChart(data) {
    console.log(String(data))
    let chartDom = document.getElementById('barChart');
    chartDom.classList.remove('hidden');
    if (!chartDom) {
        console.error("Div with id 'barChart' not found.");
        return;
    }
    if (typeof echarts === 'undefined') {
        console.error("ECharts library is not loaded.");
        return;
    }

    chartDom.style.width = '100%';
    chartDom.style.height = '400px';

    let myChart = echarts.init(chartDom);
    let option = {
        xAxis: {
            type: 'category',
            data: ['Zero-Shot', 'Few-Shot', 'Chain-of-Thought', 'Generate Knowledge', 'Self-Consistency', 'Tree of Thought'],
            axisLabel: {
                interval: 0 // Show all labels
            }
        },
        yAxis: {
            type: 'value',
            max: 100
        },
        series: [
            {
                data: [
                    { value: data?.zero_shot ? data.zero_shot * 100 : 0, itemStyle: { color: '#005C66' } },
                    { value: data?.few_shot ? data.few_shot * 100 : 0, itemStyle: { color: '#00A2AC' } },
                    { value: data?.chain_of_thought ? data.chain_of_thought * 100 : 0, itemStyle: { color: '#00F2CE' } },
                    { value: data?.generate_knowledge ? data.generate_knowledge * 100 : 0, itemStyle: { color: '#023C4C' } },
                    { value: data?.self_consistency ? data.self_consistency * 100 : 0, itemStyle: { color: '#077897' } },
                    { value: data?.tree_of_thoughts ? data.tree_of_thoughts * 100 : 0, itemStyle: { color: '#008DF2' } },
                ],
                type: 'bar',
                showBackground: true,
                backgroundStyle: {
                    color: 'rgba(180, 180, 180, 0.2)'
                },
                label: {
                    show: true,
                    position: 'top',
                    color: '#333',
                    fontWeight: 'bold',
                    formatter: '{c}%'
                }
            }
        ],
        toolbox: {
            show: true,
            feature: {
                saveAsImage: {
                    show: true,
                    name: 'benchmarking', // Optional: customize the filename
                    type: 'png' // Optional: specify image type (png, jpeg, etc.)
                }
            }
        },
    };
    myChart.setOption(option);
}

function getCookie(name) {
    let value = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let cookie of cookies) {
            cookie = cookie.replace(' ', '')
            const [cookieAttr, cookieValue] = cookie.split('=');
            if (cookieAttr == name) {
                value = cookieValue;
                break;
            }
        }
    }

    return value;
}

// Função para iniciar o processo
async function startProcessing() {
    const evaluateForm = document.getElementById('evaluateForm');
    const titleResult = document.getElementById('titleResult');
    titleResult.innerText = `Aguardando...`;
    document.getElementById('evaluateButton').querySelector('#loading')
        .classList.remove('hidden');
    document.getElementById('evaluateButton').disabled = true;
    const response = await fetch('/evaluation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: new URLSearchParams(new FormData(evaluateForm)).toString(),
    });


    const data = await response.json();
    const taskId = data.task_id;
    console.log(`Tarefa iniciada com ID: ${taskId}`);
    // localStorage.setItem('taskId', taskId);

    // Começa a verificar o status a cada 5 segundos
    checkStatus(taskId);
}

// Função para verificar o status
function checkStatus(taskId) {
    const interval = setInterval(async () => {
        const response = await fetch(`/evaluation/check/${taskId}/`);
        const data = await response.json();

        const titleResult = document.getElementById('titleResult');
        const progressElement = document.getElementById('percentageProgressElement');
        const chartDom = document.getElementById('barChart');
        chartDom.classList.add('hidden');

        if (data.status === 'PENDING') {
            titleResult.innerText = `Aguardando...`;
            progressElement.classList.remove('relative');
            progressElement.classList.add('hidden');
        }

        if (data.status === 'PROGRESS') {
            progressElement.classList.remove('hidden');
            progressElement.classList.add('relative');
            const progressCircle = document.getElementById('percentageProgressCircle');
            const progressText = document.getElementById('percentageProgressText');

            titleResult.innerText = `Processando... (${data.progress.current} de ${data.progress.total})`;

            progressText.innerText = `${data.progress.percent.toFixed(1).replace('.', ',')}%`;
            progressCircle.setAttribute('stroke-dashoffset', 100 - data.progress.percent);
        }

        // Se a tarefa estiver concluída ou falhou, para de verificar
        if (data.status === 'SUCCESS' || data.status === 'FAILURE') {
            progressElement.classList.remove('relative');
            progressElement.classList.add('hidden');
            clearInterval(interval);
            if (data.status === 'SUCCESS') {
                document.getElementById('evaluateButton').querySelector('#loading')
                    .classList.add('hidden');
                document.getElementById('evaluateButton').disabled = false;
                titleResult.innerText = `Resultados do Benchmarking`;
                renderBarChart(data.result);
            } else {
                console.error('Erro:', data.error);
                titleResult.innerText = `Avaliação falhou, tente novamente.`;
            }
        }
    }, 1000); // Verifica a cada 1 segundo
}

// document.addEventListener('DOMContentLoaded', function () {
//     const taskId = localStorage.getItem('taskId');
//     if (taskId) {
//         checkStatus(taskId);
//     }
// });