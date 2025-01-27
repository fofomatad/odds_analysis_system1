# Sistema de Análise NBA - Estratégia Holzhauer

Sistema avançado para análise de jogos NBA em tempo real, inspirado na estratégia de James Holzhauer.

## Características Principais

### 1. Análise de Comportamento
- Rastreamento de reações emocionais
- Análise de linguagem corporal
- Identificação de padrões de comportamento
- Previsão de desempenho baseada em fatores psicológicos

### 2. Análise de Sequências
- Identificação de padrões de eventos
- Cálculo de probabilidades de explosão/queda
- Detecção de gatilhos de desempenho
- Previsões para próximos minutos

### 3. Análise de Correlações
- Identificação de eventos correlacionados
- Cálculo de impactos combinados
- Multiplicadores dinâmicos
- Recomendações baseadas em correlações

### 4. Dashboard em Tempo Real
- Visualização de estados emocionais
- Gráficos de tendências
- Alertas de oportunidades
- Atualizações automáticas

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd odds_analysis_system
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## Uso

1. Inicie o servidor:
```bash
python app.py
```

2. Acesse o dashboard:
```
http://localhost:5000/
```

3. Para análise de jogadores:
```
http://localhost:5000/players
```

## Estrutura do Projeto

```
odds_analysis_system/
├── app.py                 # Aplicação principal
├── config.py             # Configurações
├── requirements.txt      # Dependências
├── README.md            # Este arquivo
├── alerts.py            # Sistema de alertas
├── odds_history.py      # Histórico de odds
├── player_stats.py      # Análise de estatísticas
├── player_behavior_tracker.py  # Rastreador de comportamento
├── holzhauer_strategy.py      # Implementação da estratégia
├── data/                # Dados armazenados
├── logs/               # Arquivos de log
└── templates/          # Templates HTML
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE.md para detalhes. 