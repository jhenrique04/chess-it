# ChessCV Project

## Descrição
Este projeto tem como objetivo realizar o reconhecimento de tabuleiros de xadrez utilizando um modelo YOLOv8 treinado para identificar as peças e suas posições. Ele é dividido em três principais componentes:

1. **chessCV** - Scripts responsáveis pelo processamento de imagem e execução do modelo de reconhecimento.
2. **frontend** - Aplicação frontend desenvolvida em React para exibição das informações processadas.
3. **yolo** - Modelo YOLOv8 treinado para a detecção das peças no tabuleiro.

## Estrutura do Projeto
```
├── chessCV
│   ├── cv_chess.py  # Script principal de reconhecimento
│   ├── cv_chess_functions.py  # Funções auxiliares para processamento
│   ├── api.py  # API em Flask para comunicação com o frontend
│
├── frontend
│   ├── src/  # Código-fonte do frontend em React
│   ├── public/
│   ├── package.json  # Dependências do projeto frontend
│
├── yolo
│   ├── datasets/  # Pasta referente ao dataset
│   ├── models/  # Arquivo do modelo
│   ├── runs/  # Treinamentos feitos usando o modelo
│
├── requirements.txt  # Dependências do projeto
└── README.md  # Este arquivo
```

## Instalação e Execução
### Pré-requisitos
Certifique-se de ter instalado:
- Python 3.8
- Node.js e npm (para o frontend)
- Dependências do projeto (definidas em `requirements.txt`)

### Configuração e Execução do Backend (chessCV)
```sh
# Criar e ativar um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # No Windows use: .venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar API Flask
python chessCV/api.py
```

### Configuração e Execução do Frontend
```sh
cd frontend
npm install  # Instalar dependências
npm start  # Rodar o frontend
```

## Uso
1. Inicie o backend para processar imagens do tabuleiro de xadrez.
2. Abra o frontend para visualizar a posição das peças em tempo real.
3. O modelo YOLOv8 é usado internamente para detecção e reconhecimento.

## Contribuição
Caso queira contribuir, sinta-se à vontade para abrir uma issue ou um pull request.
