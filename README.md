# Projeto de ETL com Airflow

Este é um README para um projeto ETL (Extração, Transformação, Carregamento) usando o Apache Airflow para extrair dados de dois bancos de dados, realizar transformações nos dados e carregar os dados transformados em um datalake MongoDB. O projeto utiliza o Docker Compose para configurar a infraestrutura necessária.

## Visão Geral do Projeto

### Tecnologias Utilizadas

- [Apache Airflow](https://airflow.apache.org/): Uma plataforma de código aberto para orquestrar fluxos de trabalho e pipelines de dados complexos.
- [PostgreSQL](https://www.postgresql.org/): Um sistema de banco de dados relacional de código aberto.
- [Redis](https://redis.io/): Usado como um servidor de mensagens para o CeleryExecutor do Airflow.
- [MongoDB](https://www.mongodb.com/): Um banco de dados de documentos NoSQL para armazenar dados não estruturados.

### Docker Compose

O projeto utiliza o Docker Compose para configurar os serviços necessários:

- PostgreSQL: Um banco de dados para extração de dados.
- Redis: Usado como um servidor de mensagens para o CeleryExecutor do Airflow.
- Airflow (Worker, Scheduler e Webserver): Usado para orquestrar e gerenciar o fluxo de trabalho ETL.
- MongoDB: O datalake para armazenar os dados transformados.

## Começando

1. **Pré-requisitos**

   - [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/install/) instalados em sua máquina.

2. **Clonar o Repositório**

   ```bash
   git clone git@ssh.dev.azure.com:v3/lds-ifce/multi-recommendation/etl
   cd etl
   ```

3. **Docker Compose**

   Execute o seguinte comando para iniciar os serviços definidos em `docker-compose.yml`:

   ```bash
   docker-compose up -d
   ```

4. **Acessar a Interface Web do Airflow**

   Abra seu navegador da web e acesse [http://localhost:8080](http://localhost:8080) para acessar a interface web do Airflow. Você pode monitorar e gerenciar seus fluxos de trabalho ETL a partir daqui.

5. **Configuração**

   - Os detalhes de conexão do PostgreSQL e do MongoDB devem ser configurados em seus arquivos DAG do Airflow (localizados no diretório `dags`).
   - Defina seu fluxo de trabalho ETL no Airflow criando DAGs (Grafos Direcionados Acíclicos).

6. **Monitoramento e Registro**

   O Airflow oferece recursos extensivos de monitoramento e registro. Você pode visualizar registros de tarefas, status e detalhes de execução por meio da interface web.

## Fluxo de Trabalho ETL

O fluxo de trabalho ETL do projeto pode ser resumido da seguinte forma:

1. **Extração**: Os dados são extraídos de dois bancos de dados PostgreSQL.

2. **Transformação**: Os dados extraídos são transformados de acordo com a lógica de negócios. Isso é definido em seus DAGs do Airflow.

3. **Carregamento**: Os dados transformados são carregados em um datalake MongoDB.

## Serviços do Docker Compose

- **PostgreSQL**: Atua como o banco de dados de origem para extração de dados. Você pode acessá-lo na porta 5432.

- **Redis**: Usado como um servidor de mensagens para o CeleryExecutor do Airflow.

- **Airflow (Worker, Scheduler, Webserver)**: Orquestra e gerencia o fluxo de trabalho ETL. Acesse a interface web do Airflow em [http://localhost:8080](http://localhost:8080).

- **MongoDB**: O datalake de destino para armazenar os dados transformados. Você pode acessá-lo na porta 27017.

## Estrutura de Diretórios

- `dags/`: Coloque seus arquivos DAG do Airflow aqui, onde você define os fluxos de extração, transformação e carregamento de dados.

## Personalização

Você pode personalizar este projeto modificando o seguinte:

- DAGs do Airflow no diretório `dags/` para especificar sua lógica de extração, transformação e carregamento de dados.
- Conexões de banco de dados, credenciais e outras configurações em seus DAGs.
- Serviços adicionais, como validação de dados e tratamento de erros.

## Limpeza

Para parar e remover os contêineres Docker Compose, execute:

```bash
docker-compose down
```

## Conclusão

Este README fornece uma visão geral do seu projeto ETL usando o Apache Airflow e o Docker Compose. Você pode adaptar o projeto às suas necessidades específicas de extração, transformação e carregamento de dados. Certifique-se de explorar a documentação e os recursos do Airflow para criar e gerenciar fluxos de trabalho complexos. Bom trabalho com seu ETL!