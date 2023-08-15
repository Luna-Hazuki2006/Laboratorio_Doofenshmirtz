const charts = document.getElementById('charts')

function precios() {
    charts.innerHTML = ''
    const ctx = document.createElement('canvas')
    ctx.id = 'myChart'
    charts.appendChild(ctx)
    const nombre = document.getElementById('precios')
    let data = {}
    let listaNombres = []
    let cantidades = []
    for (const datos of nombre.children) {
        listaNombres.push(datos.id)
        cantidades.push(datos.children.length)
    }
    data.nombres = listaNombres
    data.cantidades = cantidades
    new Chart(ctx, {
        type: 'bar',
            data: {
                labels: data.nombres,
                datasets: [{
                    label: 'Precios',
                    data: data.cantidades,
                    borderWidth: 1
                }]
            },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function categorias() {
    charts.innerHTML = ''
    const ctx = document.createElement('canvas')
    ctx.id = 'myChart'
    charts.appendChild(ctx)
    const nombre = document.getElementById('categorias')
    let data = {}
    let listaNombres = []
    let cantidades = []
    for (const datos of nombre.children) {
        listaNombres.push(datos.id)
        cantidades.push(datos.children.length)
    }
    data.nombres = listaNombres
    data.cantidades = cantidades
    new Chart(ctx, {
        type: 'bar',
            data: {
                labels: data.nombres,
                datasets: [{
                    label: 'Categorias',
                    data: data.cantidades,
                    borderWidth: 1
                }]
            },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    }); 
}