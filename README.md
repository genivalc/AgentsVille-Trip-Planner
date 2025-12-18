# 🌍 AgentsVille Trip Planner

Sistema inteligente de planejamento de viagens com IA que gera itinerários personalizados baseados nos interesses dos viajantes, dados climáticos e atividades disponíveis.

## 🚀 Tecnologias

### Backend
- **Python 3.x** - Linguagem principal
- **Flask 3.0.0** - Framework web
- **OpenAI API** - Geração de itinerários com IA
- **Pydantic 2.11.7** - Validação de dados
- **Pandas 2.3.0** - Manipulação de dados
- **Flask-CORS** - Suporte a CORS

### Frontend
- **Next.js 14** - Framework React
- **TypeScript** - Tipagem estática
- **React 18** - Interface de usuário
- **Bootstrap 5.3.8** - Framework CSS
- **Axios** - Cliente HTTP

## 📁 Estrutura do Projeto

```
AgentsVille-Trip-Planner/
├── backend/
│   ├── models/
│   │   └── schemas.py          # Modelos Pydantic
│   ├── services/
│   │   ├── ai_service.py       # Integração com OpenAI
│   │   ├── weather_service.py  # Dados climáticos
│   │   ├── activities_service.py # Atividades disponíveis
│   │   └── image_service.py    # Galeria de imagens
│   ├── utils/
│   │   └── validators.py       # Validações
│   ├── app.py                  # Aplicação Flask
│   ├── requirements.txt        # Dependências Python
│   └── .env                    # Variáveis de ambiente
├── frontend/
│   ├── app/
│   │   ├── components/
│   │   │   ├── TravelForm.tsx  # Formulário de viagem
│   │   │   └── ItineraryDisplay.tsx # Exibição do itinerário
│   │   ├── services/
│   │   │   └── api.ts          # Cliente da API
│   │   ├── globals.css         # Estilos globais
│   │   ├── layout.tsx          # Layout principal
│   │   └── page.tsx            # Página inicial
│   ├── package.json            # Dependências Node.js
│   └── tsconfig.json           # Configuração TypeScript
└── LICENSE                     # Licença MIT
```

## ⚙️ Instalação e Configuração

### Backend

1. **Clone o repositório:**
```bash
git clone <repository-url>
cd AgentsVille-Trip-Planner/backend
```

2. **Crie um ambiente virtual:**
```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
```bash
# Crie um arquivo .env na pasta backend
OPENAI_API_KEY=sua_chave_openai
OPENAI_BASE_URL=https://api.openai.com/v1
```

5. **Execute o servidor:**
```bash
python app.py
```

O backend estará disponível em `http://localhost:5000`

### Frontend

1. **Navegue para a pasta frontend:**
```bash
cd ../frontend
```

2. **Instale as dependências:**
```bash
npm install
# ou
pnpm install
```

3. **Execute o servidor de desenvolvimento:**
```bash
npm run dev
# ou
pnpm dev
```

O frontend estará disponível em `http://localhost:3000`

## 🎯 Funcionalidades

### ✅ Implementadas

- **Geração de Itinerários Inteligentes**: IA cria planos personalizados
- **Formulário Interativo**: Coleta dados dos viajantes e preferências
- **Validação de Dados**: Verificação completa de informações
- **Integração Climática**: Dados meteorológicos para planejamento
- **Sistema de Atividades**: Recomendações baseadas em interesses
- **Histórico de Viagens**: Armazenamento e consulta de planos anteriores
- **Modificação de Itinerários**: Alterações via IA em tempo real
- **Interface Responsiva**: Design adaptável com Bootstrap
- **Galeria de Imagens**: Visualização do destino

### 🔄 Interesses Suportados

- Arte, Culinária, Comédia, Dança
- Fitness, Jardinagem, Trilha, Filmes
- Música, Fotografia, Leitura, Esportes
- Tecnologia, Teatro, Tênis, Escrita

## 🌐 API Endpoints

### Principais Rotas

- `GET /health` - Verificação da API
- `POST /api/generate-itinerary` - Gerar novo itinerário
- `POST /api/modify-itinerary/<trip_id>` - Modificar itinerário existente
- `GET /api/trip-history` - Histórico de viagens
- `GET /api/trip/<trip_id>` - Detalhes de viagem específica
- `GET /api/weather/<city>/<date>` - Informações climáticas
- `GET /api/activities` - Atividades disponíveis

### Exemplo de Requisição

```json
{
  "travelers": [
    {
      "name": "João Silva",
      "age": 30,
      "interests": ["art", "music", "photography"]
    }
  ],
  "destination": "Paris",
  "date_of_arrival": "2024-06-15",
  "date_of_departure": "2024-06-20",
  "budget": 5000
}
```

## 🎨 Interface

### Componentes Principais

- **TravelForm**: Formulário para dados da viagem
- **ItineraryDisplay**: Exibição detalhada do itinerário
- **API Service**: Cliente HTTP para comunicação

### Estilização

- Tema escuro personalizado
- Bootstrap 5.3.8 para responsividade
- Componentes modernos e intuitivos

## 🔧 Scripts Disponíveis

### Backend
```bash
python app.py          # Servidor de desenvolvimento
```

### Frontend
```bash
npm run dev           # Servidor de desenvolvimento
npm run build         # Build para produção
npm run start         # Servidor de produção
```

## 📊 Modelos de Dados

### Principais Schemas

- **VacationInfo**: Informações da viagem
- **Traveler**: Dados do viajante
- **TravelPlan**: Plano de viagem gerado
- **Activity**: Atividade recomendada
- **Weather**: Dados climáticos

## 🔒 Segurança

- Validação rigorosa de entrada
- Sanitização de dados
- Tratamento de erros robusto
- Variáveis de ambiente para credenciais

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Genival Neto** - Desenvolvedor Principal

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte e dúvidas, abra uma issue no repositório do projeto.

---

**AgentsVille Trip Planner** - Transformando sonhos de viagem em realidade com inteligência artificial! 🚀✈️