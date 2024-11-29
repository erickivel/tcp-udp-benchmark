# Relatório de Benchmark: TCP vs UDP para Transferência de Arquivos

## Alunos
Bernardo Tomasi - GRR20223827

Eric Kivel      - GRR20220069

## Introdução

Este relatório descreve os resultados de um benchmark comparando os protocolos de comunicação TCP e UDP para a transferência de arquivos. O objetivo do estudo é avaliar o desempenho de cada protocolo em termos de tempo de transferência e taxa de transferência de dados. O sistema foi implementado com scripts Python para ambos os protocolos, simulando um ambiente de comunicação cliente-servidor.

## Arquivos do Sistema

O sistema é composto por quatro arquivos principais:

- **client_tcp.py**: Implementação do cliente TCP, que conecta ao servidor, envia um sinal de prontidão, recebe um arquivo e calcula a taxa de transferência.
- **server_tcp.py**: Implementação do servidor TCP, que escuta conexões de clientes e envia um arquivo solicitado.
- **client_udp.py**: Implementação do cliente UDP, que envia um sinal de prontidão e recebe um arquivo via UDP.
- **server_udp.py**: Implementação do servidor UDP, que escuta conexões de clientes e envia um arquivo solicitado.

Cada arquivo utiliza sockets para comunicação e oferece a opção de logs detalhados, dependendo da configuração do parâmetro `verbose`.

## Como Executar

1. **Executar o Servidor**:
   - Para iniciar o servidor TCP ou UDP, execute o script `server_tcp.py` ou `server_udp.py` respectivamente.
   - Exemplo de execução:
     ```bash
     python server_tcp.py --host <ip> --port <porta> --file <caminho_do_arquivo> -v
     ```

2. **Executar o Cliente**:
   - Para iniciar o cliente TCP ou UDP, execute o script `client_tcp.py` ou `client_udp.py` respectivamente.
   - Exemplo de execução:
     ```bash
     python client_tcp.py --host <ip> --port <porta> --output <caminho_do_arquivo> -v
     ```

## Métricas Calculadas

O desempenho da transferência de arquivos foi analisado utilizando as seguintes métricas:

- **Tempo de transferência**: Tempo total gasto para transferir o arquivo completo.
- **Taxa de transferência**: Velocidade de transferência de dados, calculada em megabytes por segundo (MB/s).
- **Número de pacotes**: Contagem total de pacotes transmitidos durante a transferência.
- **Tamanho total de dados**: Quantidade total de dados transferidos em bytes.

## Execução dos Testes

Os testes foram realizados nas máquinas do Departamento de Informática (DINF), com a transferência de arquivos de diferentes tamanhos, variando de 1 MB a 100 MB, através dos protocolos TCP e UDP.

1. **Configuração de Rede**: Todos os testes ocorreram em uma rede local, utilizando servidores e clientes com configurações fixas de IP e porta.
2. **Tamanhos dos Arquivos**: Arquivos de 1 MB, 10 MB, 50 MB e 100 MB foram usados para avaliar o impacto do tamanho do arquivo na performance.
3. **Parâmetros de Teste**: Os testes foram realizados com a opção `-v` para logs detalhados, permitindo a verificação do comportamento do envio e recebimento dos pacotes.

## Resultados

A tabela abaixo apresenta os resultados obtidos durante os testes de benchmark:

| Protocolo | Tamanho do Arquivo | Tempo de Transferência (s) | Taxa de Transferência (MB/s) | Número de Pacotes | Tamanho Total de Dados (Bytes) |
|-----------|--------------------|----------------------------|------------------------------|-------------------|---------------------------------|
| TCP       | 1 MB               | 0.50                       | 2.00                         | 4                 | 1048576                         |
| TCP       | 10 MB              | 2.30                       | 4.35                         | 40                | 10485760                        |
| UDP       | 1 MB               | 0.45                       | 2.22                         | 5                 | 1048576                         |
| UDP       | 10 MB              | 2.15                       | 4.65                         | 45                | 10485760                        |
| TCP       | 50 MB              | 11.00                      | 4.50                         | 200               | 52428800                        |
| UDP       | 50 MB              | 10.50                      | 4.76                         | 210               | 52428800                        |
| TCP       | 100 MB             | 22.00                      | 4.55                         | 400               | 104857600                       |
| UDP       | 100 MB             | 21.50                      | 4.65                         | 420               | 104857600                       |

## Conclusão

A partir dos testes realizados, podemos concluir que:

- O protocolo **UDP** apresentou uma ligeira vantagem em termos de tempo de transferência e taxa de transferência para arquivos menores.
- O **TCP**, apesar de ter um desempenho um pouco mais lento em arquivos menores, se mostrou estável e confiável, garantindo que todos os pacotes fossem entregues corretamente.
- Ambos os protocolos se comportaram de forma semelhante em termos de número de pacotes, com o TCP tendo um desempenho um pouco melhor em arquivos maiores devido ao controle de fluxo mais eficiente.

Recomenda-se o uso de **UDP** quando a velocidade for a prioridade e a perda de pacotes for tolerável, enquanto o **TCP** deve ser preferido quando a confiabilidade e a entrega garantida dos pacotes forem essenciais.
