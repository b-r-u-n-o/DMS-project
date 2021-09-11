# Projeto de Engenharia de dados com AWS DMS

Esse projeto visa reproduzir situações que fazem parte do dia a dia de Engenheiro de dados.
- Criar uma instância do Postgres no RDS (usando a free-tier)
- Desenvolver código Python para popular o DB com dados fake
- Usar o DMS para replicar os dados de uma instância Postgres:
  - Para o S3 
  - Para o Redshift (ou outra instância de banco de dados) ***
## Fluxo

 ![Fluxo-RDS-DMS](img/escopo-projeto.png)



## Steps

 1. Criar Instância de Banco de Dados no RDS
    a. Configurar o Parameter Group

    > rds.logical_replication=1 # ativa a replicação para o binlog
    wal_sender_timeout=0 #timeout setado para 0

    b.  Ajustar o postgres para Parameter group definido
2. Desenvolver código Python para ingestão dos dados no database
3. Criar cluster Redshift
4. Criar bucket S3
5. Criar replicação com DMS
    - 5.1 Configurar endpoint de origem
    - 5.2 Configurar endpoint de destino Redshift
    - 5.3 Configurar endpoint de destino S3
        - a. Criar política no IAM:
            - i. ListBucket
            - ii. PutObjectTagging
            - iii. DeleteObject
            - iv. PutObject
        - b. Criar função no IAM com base na política criada
            - i. atribuir um nome para vinculado ao uso (para facilitar a identificação)
        - c. Configurar os atributos de inserção no bucket
            - i. config Atributos do S3 para o DMS

            ```sql
            dataFormat=parquet;timestampColumnName=extracted_;maxFileSize=maxFileSize=131072\n
            includeOpForFullLoad=true;cdcMaxBatchInterval=180;
            ```

        - d. Criar a task de replicação