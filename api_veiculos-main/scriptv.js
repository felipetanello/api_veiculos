const listaVeiculos = document.getElementById('lista-veiculos');
const formVeiculo = document.getElementById('form-veiculo');

function listarVeiculos() {
  fetch('http://127.0.0.1:5000/veiculos')
    .then(response => response.json())
    .then(veiculos => {
      listaVeiculos.innerHTML = ''; 
      veiculos.forEach(veiculo => {
        const item = document.createElement('li');
        item.innerHTML = `
          <span><strong>${veiculo.marca} ${veiculo.modelo}</strong></span>
          <span>Ano: ${veiculo.ano}</span>
          <span>Preço: R$ ${veiculo.preco.toFixed(2)}</span>
        `;
        listaVeiculos.appendChild(item);
      });
    })
    .catch(error => {
      console.error('Erro ao listar veículos:', error);
      alert('Falha ao se conectar com a API.');
    });
}

formVeiculo.addEventListener('submit', function(event) {
  event.preventDefault();

  const dadosVeiculo = {
    marca: document.getElementById('marca').value,
    modelo: document.getElementById('modelo').value,
    ano: document.getElementById('ano').value,
    preco: document.getElementById('preco').value
  };

  fetch('http://127.0.0.1:5000/veiculos', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dadosVeiculo)
  })
  .then(response => response.json())
  .then(novoVeiculo => {
    console.log('Veículo cadastrado:', novoVeiculo);
    listarVeiculos(); 
    formVeiculo.reset(); 
  })
  .catch(error => {
    console.error('Erro ao cadastrar veículo:', error);
    alert('Falha ao cadastrar veículo.');
  });
});

listarVeiculos();
