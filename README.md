# Trabalho Prático de Redes de Computadores II - Turma 2024/2
# **Relatório de Benchmark: TCP vs UDP**

## Alunos
- **Bernardo Tomasi** - GRR20223827
- **Eric Kivel** - GRR20220069

## Introdução

Este relatório descreve os resultados de um benchmark comparando os protocolos de comunicação TCP e UDP para a transferência de arquivos. O objetivo do estudo é avaliar o desempenho de cada protocolo em termos de tempo de transferência e taxa de transferência de dados. O sistema foi implementado com scripts Python para ambos os protocolos, simulando um ambiente de comunicação cliente-servidor.

## Arquivos do Sistema

O sistema é composto por quatro arquivos principais:

- **[tcp.client.py.txt - Download](assets/tcp.client.py.txt)**: Implementação do cliente TCP, que conecta ao servidor, envia um sinal de prontidão, recebe um arquivo e calcula a taxa de transferência. - <a href="assets/tcp.client.py.txt" target="_blank">Ou abra o arquivo aqui</a>
- **[tcp.server.py.txt - Download](assets/tcp.server.py.txt)**: Implementação do servidor TCP, que escuta conexões de clientes e envia um arquivo solicitado. - <a href="assets/tcp.server.py.txt" target="_blank">Ou abra o arquivo aqui</a>
- **[udp.client.py.txt - Download](assets/udp.client.py.txt)**: Implementação do cliente UDP, que envia um sinal de prontidão e recebe um arquivo via UDP. - <a href="assets/udp.client.py.txt" target="_blank">Ou abra o arquivo aqui</a>
- **[udp.server.py.txt - Download](assets/udp.server.py.txt)**: Implementação do servidor UDP, que escuta conexões de clientes e envia um arquivo solicitado. - <a href="assets/udp.server.py.txt" target="_blank">Ou abra o arquivo aqui</a>

Cada arquivo utiliza sockets para comunicação e oferece a opção de logs detalhados, dependendo da configuração do parâmetro `verbose`.

## Como Executar

1. **Executar o Servidor**:
   - Para iniciar o servidor TCP ou UDP, execute o script `tcp.server.py` ou `udp.server.py` respectivamente.
   - Exemplo de execução:
     ```bash
     python tcp.server.py --host <ip> --port <porta> -v
     ```

2. **Executar o Cliente**:
   - Para iniciar o cliente TCP ou UDP, execute o script `tcp.client.py` ou `udp.client.py` respectivamente.
   - Exemplo de execução:
     ```bash
     python tcp.client.py --host <ip> --port <porta> --file <arquivo_solicitado> --buffer <tamanho_buffer> -v
     ```

## Métricas Calculadas

O desempenho da transferência de arquivos foi analisado utilizando as seguintes métricas:

- **Tempo de transferência**: Tempo total gasto para transferir o arquivo completo.
- **Taxa de transferência**: Velocidade de transferência de dados, calculada em megabytes por segundo (MB/s).
- **Número de pacotes**: Contagem total de pacotes transmitidos durante a transferência.
- **Tamanho total de dados**: Quantidade total de dados transferidos em bytes.


## Execução dos Testes

Os testes foram realizados nas máquinas do Departamento de Informática (DINF), com a transferência de arquivos de diferentes tamanhos, variando de 100 MB a 2 GB, através dos protocolos TCP e UDP.
Para realizar o teste foi utilizado um script chamado `test_client.sh` (<a href="assets/test_client.sh.txt" target="_blank">Aqui</a>) para automatizar a execução de testes com diferentes tamanhos de arquivo e tamanhos de buffer. O servidor, enquanto isso, ficava ligado escutando as conexões.

1. **Configuração de Rede**: Todos os testes ocorreram em uma rede local, utilizando servidores e clientes com configurações fixas de IP e porta.
2. **Tamanhos dos Arquivos**: Arquivos de 100 MB, 200 MB, 500 MB, 1 GB e 2 GB foram usados para avaliar o impacto do tamanho do arquivo na performance.
3. **Tamanho do Buffer**: Buffer de 1024B, 2048B, 4096B, 8192B, 16384B e 32768B para cada tamanho de arquivo foram usados para avaliar o impacto do tamanho do buffer na performance.

## Resultados

### Resultados em CSV  
Os resultados completos dos testes estão disponíveis nos arquivos CSV, que podem ser acessados nos links abaixo:  

- <a href="assets/metricas_tcp.csv.txt" target="_blank">Resultados TCP</a>
- <a href="assets/metricas_udp.csv.txt" target="_blank">Resultados UDP</a>

Esses arquivos contêm informações detalhadas sobre o desempenho de cada protocolo, incluindo o tempo de transferência, taxa de transferência, e número de pacotes para diferentes tamanhos de arquivos e buffers.  

- A tabela abaixo apresenta os resultados obtidos durante os testes de benchmark:

| Total de Bytes Recebidos (MB/GB) | Protocolo | Média do Tempo Decorrido (s) | Média do Número de Pacotes | Média da Taxa de Transferência (MB/s) |
|----------------------------------|-----------|------------------------------|----------------------------|-------------------------------------|
| 100 MB                           | TCP       | 0.99                         | 28,368                     | 101.33                              |
| 100 MB                           | UDP       | 2.98                         | 6,400                      | 33.58                               |
| 200 MB                           | TCP       | 1.96                         | 70,066                     | 102.12                              |
| 200 MB                           | UDP       | 3.94                         | 41,395                     | 50.73                               |
| 500 MB                           | TCP       | 4.91                         | 134,217                    | 101.78                              |
| 500 MB                           | UDP       | 6.79                         | 64,800                     | 73.56                               |
| 1 GB                             | TCP       | 10.08                        | 282,843                    | 101.55                              |
| 1 GB                             | UDP       | 11.84                        | 104,857                    | 86.48                               |
| 2 GB                             | TCP       | 21.32                        | 1,328,780                  | 96.05                               |
| 2 GB                             | UDP       | 21.75                        | 901,052                    | 93.69                               |


- **Comparação de Número de Pacotes:**

O TCP enviou um número maior de pacotes do que o UDP para todos os tamanhos de buffer testados. Essa diferença é mais notável nos buffers menores, como 1024 bytes, mas diminui à medida que o tamanho do buffer aumenta.

![comparacao_pacotes](assets/comparacao_pacotes.png)

- **Comparação de Throughput: TCP vs UDP:**

O throughput do TCP é consistentemente mais alto do que o do UDP, independentemente do tamanho do buffer. O TCP atinge cerca de 100 MB/s, enquanto o UDP fica próximo a 50 MB/s.

![comparacao_throughput](assets/comparacao_throughput.png)

- **Tempo Decorrido vs Tamanho do Buffer:**

O tempo de transmissão aumenta com o tamanho do buffer para ambos os protocolos. O UDP apresenta tempos de transmissão ligeiramente maiores em comparação ao TCP, especialmente em buffers maiores.

![tempo_vs_buffer](assets/tempo_vs_buffer.png)

- **Throughput vs Tamanho do Arquivo:**

O throughput do TCP é consistentemente mais alto do que o do UDP, porém conforme a tamanho dos arquivos aumentam o UDP se aproxima do TCP.

![throughput_vs_tamanho_arquivo](assets/throughput_vs_tamanho_arquivo.png)

- **Throughput vs Tamanho do Buffer:**

O throughput do TCP é maior que o UDP independentemente do buffer.

![throughput_vs_tamanho_buffer](assets/throughput_vs_tamanho_buffer.png)

## Logs

Durante a execução dos testes, os logs detalhados fornecem informações cruciais sobre o andamento das transferências e o comportamento de cada protocolo. A seguir, alguns exemplos dos logs gerados durante a execução do protocolo TCP e UDP:

### Log Exemplo de Cliente TCP

```
INFO:CLIENTE_TCP:Cliente TCP conectando a 10.254.223.42:8000
INFO:CLIENTE_TCP:Conectado ao servidor.
INFO:CLIENTE_TCP:Solicitação do arquivo '100mb.dat' enviada.
INFO:CLIENTE_TCP:Métricas salvas no arquivo CSV 'metricas_tcp.csv'.
INFO:CLIENTE_TCP:Integridade dos dados: Aprovada
INFO:CLIENTE_TCP:Bytes perdidos: 0
INFO:CLIENTE_TCP:Arquivo recebido em 0.98 segundos. Taxa: 102.52 MB/s
INFO:CLIENTE_TCP:Conexão encerrada.
```

### Log Exemplo de Cliente UDP

```
INFO:CLIENTE_UDP:Cliente UDP conectando a 10.254.223.42:8000
INFO:CLIENTE_UDP:Sinal de prontidão (READY) enviado ao servidor.
INFO:CLIENTE_UDP:Servidor está pronto para enviar o arquivo.
INFO:CLIENTE_UDP:Timeout atingido. Transferência concluída.
INFO:CLIENTE_UDP:Arquivo recebido em 2.96 segundos.
INFO:CLIENTE_UDP:Tamanho total recebido: 104857600 bytes.
INFO:CLIENTE_UDP:Taxa de transferência: 33.81 MB/s.
INFO:CLIENTE_UDP:Métricas salvas no arquivo CSV 'metricas_udp.csv'.
INFO:CLIENTE_UDP:Integridade dos dados: Aprovada
INFO:CLIENTE_UDP:Bytes perdidos: 0
INFO:CLIENTE_UDP:Execução do cliente finalizada.
```

### Log Exemplo de Servidor TCP

```
INFO:SERVIDOR_TCP:Servidor TCP inicializado em 10.254.223.42:8000.
INFO:SERVIDOR_TCP:Servidor ouvindo em 10.254.223.42:8000
INFO:SERVIDOR_TCP:Conexão aceita de ('10.254.223.43', 35436)
INFO:SERVIDOR_TCP:Preparando para enviar 'send_data/100mb.dat' com buffer de 1024 bytes.
INFO:SERVIDOR_TCP:Arquivo 'send_data/100mb.dat' enviado em 0.96 segundos. Taxa: 104.60 MB/s
INFO:SERVIDOR_TCP:Conexão encerrada.
```

### Log Exemplo de Servidor UDP

```
INFO:SERVIDOR_UDP:Servidor UDP inicializado em 10.254.223.42:8000.
INFO:SERVIDOR_UDP:Servidor ouvindo em 10.254.223.42:8000
INFO:SERVIDOR_UDP:Sinal de prontidão recebido de ('10.254.223.43', 38010). Iniciando transferência do arquivo.
INFO:SERVIDOR_UDP:Preparando para enviar 'send_data/100mb.dat' com buffer de 1024 bytes.
INFO:SERVIDOR_UDP:Arquivo 'send_data/100mb.dat' enviado em 0.95 segundos. Taxa: 104.79 MB/s
INFO:SERVIDOR_UDP:Execução do servidor finalizada.
```

### Log Exemplo com a tag --verbose

```
DEBUG:SERVIDOR_TCP:Pacote 48151 enviado, tamanho: 1024 bytes
DEBUG:SERVIDOR_TCP:Pacote 48152 enviado, tamanho: 1024 bytes
DEBUG:SERVIDOR_TCP:Pacote 48153 enviado, tamanho: 1024 bytes
DEBUG:SERVIDOR_TCP:Pacote 48154 enviado, tamanho: 1024 bytes
DEBUG:SERVIDOR_TCP:Pacote 48155 enviado, tamanho: 1024 bytes
DEBUG:SERVIDOR_TCP:Pacote 48156 enviado, tamanho: 1024 bytes
```

Esses logs são úteis para monitorar o comportamento do sistema, especialmente para identificar a quantidade de pacotes enviados e o tempo necessário para a transferência. Com a opção `-v`, o cliente e o servidor geram logs detalhados de cada pacote com o seu número e tamanho para facilitar a análise do desempenho da transferência.

## Conclusão

A partir dos testes realizados, podemos concluir que:

- O protocolo **TCP** apresentou melhor desempenho em termos de tempo de transferência, sendo mais rápido que o **UDP** para todos os tamanhos de arquivos testados. No entanto, o TCP precisou enviar um número significativamente maior de pacotes, o que reflete o seu controle mais rigoroso sobre a entrega e a confiabilidade dos dados.
  
- O **UDP** transferiu menos pacotes em comparação ao TCP, mas teve um desempenho inferior em termos de tempo de transferência e taxa de transferência, especialmente para arquivos maiores. Apesar disso, o UDP pode ser vantajoso em situações onde a perda de pacotes é aceitável e a velocidade de envio é mais importante que a confiabilidade.

Portanto, o **TCP** deve ser preferido quando a integridade e confiabilidade dos dados são essenciais, enquanto o **UDP** pode ser uma opção viável para aplicações que priorizam a velocidade e toleram perdas ou precisam de baixa sobrecarga de pacotes.
Além disso, os resultados sugerem que o melhor desempenho do TCP em throughput e tempo de transferência se deve ao seu controle de fluxo e de congestionamento, que otimiza a utilização da capacidade da rede para atingir a maior taxa de transmissão possível.
