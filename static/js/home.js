
// import * as echarts from 'echarts';


function renderBarChart() {
    let chartDom = document.getElementById('barChart');
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
            data: ['Zero-Shot', 'Few-Shot', 'Chain-of-Thought', 'Generate Knowledge', 'Self-Consistency', 'Tree of Thought']
        },
        yAxis: {
            type: 'value',
            max: 100
        },
        series: [
            {
                data: [
                    { value: 50, itemStyle: { color: '#005C66' } },
                    { value: 70, itemStyle: { color: '#00A2AC' } },
                    { value: 60, itemStyle: { color: '#00F2CE' } },
                    { value: 90, itemStyle: { color: '#023C4C' } },
                    { value: 100, itemStyle: { color: '#077897' } },
                    { value: 80, itemStyle: { color: '#008DF2' } },
                    // { value: 70, itemStyle: { color: '#FFB647' } }
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

// Função para iniciar o processo
async function startProcessing() {
    const response = await fetch('/evaluation/');
    const data = await response.json();
    const taskId = data.task_id;
    console.log(`Tarefa iniciada com ID: ${taskId}`);
    localStorage.setItem('taskId', taskId);

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

        if (data.status === 'PENDING') {
            titleResult.innerText = `Aguardando...`;
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
                titleResult.innerText = `Resultados do Benchmarking`;
                renderBarChart();
            } else {
                console.error('Erro:', data.error);
                document.getElementById('status-message').innerText = `Falhou: ${data.error}`;
            }
        }
    }, 500); // Verifica a cada 5 segundos
}


const taskId = localStorage.getItem('taskId');
if (taskId) {
    checkStatus(taskId);
}