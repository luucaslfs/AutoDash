# Canvas de Mapeamento de Fontes de Dados

## 1. Nome da Fonte de Dados

- **Nome:** Input do Usuário

## 2. Descrição da Fonte de Dados

- **Descrição:**
  A fonte de dados primária para esta aplicação é o conjunto de dados carregado diretamente pelos usuários. Estes dados podem estar em formatos CSV ou XLSX e contêm as informações que os usuários desejam visualizar e analisar. O papel desta fonte de dados é central para o funcionamento da aplicação, pois a partir dela o sistema gera automaticamente código Python para criar dashboards personalizados.

## 3. Origem dos Dados

- **Origem:**
  Os dados são originados diretamente dos usuários da aplicação, que carregam seus próprios arquivos de dados (CSV ou XLSX) através da interface web da aplicação.

## 4. Tipo de Dados

- **Tipo:**
  - Estruturados (tabelas em formato CSV ou XLSX)
  - Dados tabulares com colunas e linhas que representam variáveis e observações específicas.

## 5. Qualidade dos Dados

- **Qualidade:**
  - A qualidade dos dados depende parcialmente da entrada do usuário. A aplicação prevê a criação de scripts de limpeza, transformação e preparação dos dados quando necessário.
  - No entanto, a responsabilidade de fornecer dados relevantes é do usuário.

## 6. Métodos de Coleta dos Dados

- **Método:**
  - Upload direto através da interface do usuário na aplicação web. Os usuários selecionam e enviam seus arquivos de dados via uma funcionalidade de upload disponível no sistema.

## 7. Relevância dos Dados

- **Relevância:**
  - Altamente relevante, pois os dados fornecidos pelos usuários são a base para a geração dos dashboards. A aplicação depende inteiramente desses dados para fornecer valor ao usuário final, transformando-os em visualizações significativas e insights.
