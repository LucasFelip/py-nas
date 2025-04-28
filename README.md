# Servidor NAS Web para Termux

Uma interface web leve e responsiva para gerenciar arquivos em um dispositivo Android via Termux, inspirada no Windows Explorer e macOS Finder.

---

## 🌟 Principais Recursos

- **Upload Drag & Drop**: Arraste e solte arquivos na área de upload ou use o botão “Enviar”  
- **Criação de Pastas**: Crie novos diretórios diretamente da interface  
- **Download & Exclusão**: Baixe e exclua arquivos e pastas com um clique  
- **Navegação em Árvore**: Explore a estrutura de pastas como em um gerenciador de arquivos desktop  
- **Responsivo**: Funciona perfeitamente em telas de celular, tablet e desktop  
- **Feedback Visual**: Overlay de carregamento para operações demoradas

---

## 🛠️ Tecnologias

- **Backend**: [Flask](https://flask.palletsprojects.com/) (Python 3)  
- **Frontend**: HTML5, CSS3 (Custom Properties), JavaScript (Fetch API, Drag & Drop)  
- **Ícones**: [FontAwesome 6](https://fontawesome.com/)  
- **Execução**: Termux no Android (com Python e Git)

---

## ⚙️ Pré-requisitos

1. **Termux** instalado no seu dispositivo Android  
2. Permissão de armazenamento (via `termux-setup-storage`)  
3. Python 3 e Git instalados:
   ```bash
   pkg update && pkg install python git
4. Instalar dependências Python:
   ```bash
   pip install flask
   ```

---

## 🚀 Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/LucasFelip/servidor-nas-termux.git
   cd servidor-nas-termux
   ```

2. **Configure a pasta de armazenamento**  
   No início de `server.py`, ajuste a variável `ROOT_FOLDER` para o caminho Termux onde quer guardar os arquivos:
   ```python
   ROOT_FOLDER = '/data/data/com.termux/files/home/storage/shared/NAS'
   ```

3. **Execute o servidor**
   ```bash
   python server.py
   ```
   Acesse em: `http://localhost:8080` no navegador do Android ou de outro dispositivo na mesma rede.

---

## 📂 Estrutura do Projeto

```text
servidor-nas-termux/
├── server.py           # Lógica Flask e manipulação de arquivos
├── templates/
│   └── index.html      # Página HTML principal (Jinja2)
├── static/
│   ├── css/
│   │   └── style.css   # Estilos CSS modernos
│   ├── js/
│   │   └── main.js     # Upload, download e exclusão via Fetch API
│   └── favicon.ico     # Ícone do navegador
└── README.md           # Este arquivo
```

---

## ⚙️ Configurações Adicionais

- **Limite de upload**: em `server.py` via `UPLOAD_LIMIT_MB` (default 512 MB)
- **Porta e host**: configuráveis em `app.run(host, port)` no final de `server.py`

---

## 📞 Autor & Contato

**Lucas Felipe dos Reis Ferreira**  
Full Stack Developer | Backend Specialist  
📧 lucasfeliperis@hotmail.com
🔗 [LinkedIn](https://linkedin.com/in/lucas-ferreira-5247b1221)  
🐙 [GitHub](https://github.com/LucasFelip)  
🌐 [Portfólio](https://lucasfelipe.netlify.app)

---

## 📝 Licença

Este projeto está sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
