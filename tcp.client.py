import socket
import logging
import sys
import time
import csv
import os


class Client:
    def __init__(self, host, port, buffer_size, file_name, verbose):
        # Inicializa o cliente com os parâmetros fornecidos
        # @host - endereço IP do servidor
        # @port - número da porta do servidor
        # @buffer_size - tamanho do buffer utilizado na recepção de pacotes
        # @file_name - nome do arquivo a ser solicitado ao servidor
        # @verbose - nível de detalhamento do log (True para log detalhado)
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.file_name = file_name
        self.verbose = verbose
        self.logg = logging.getLogger("CLIENTE_TCP")

    def _init_logging(self):
        # Configura o sistema de logging com o nível adequado
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level)
        self.logg.info(f"Cliente TCP conectando a {self.host}:{self.port}")

    def _log_metrics_to_csv(
        self, total_received, elapsed_time, packet_count, throughput, actual_file_size
    ):
        # Salva métricas da transferência em um arquivo CSV
        # @total_received - total de bytes recebidos durante a transferência
        # @elapsed_time - tempo total decorrido para a transferência
        # @packet_count - número de pacotes recebidos
        # @throughput - taxa de transferência em MB/s
        # @actual_file_size - tamanho esperado do arquivo
        csv_file = "metricas_tcp.csv"
        file_exists = os.path.isfile(csv_file)

        # Calcular bytes perdidos
        bytes_lost = actual_file_size - total_received
        integridade = "Aprovada" if bytes_lost == 0 else "Falhou"

        header = [
            "Total de Bytes Recebidos",
            "Tempo Decorrido (s)",
            "Número de Pacotes",
            "Taxa de Transferência (MB/s)",
            "Tamanho Esperado (bytes)",
            "Bytes Perdidos",
            "Integridade dos Dados",
            "Tamanho do Buffer (bytes)",
        ]

        row = [
            total_received,
            round(elapsed_time, 2),
            packet_count,
            round(throughput, 2),
            actual_file_size,
            bytes_lost,
            integridade,
            self.buffer_size,
        ]

        with open(csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(
                    header
                )  # Escreve o cabeçalho apenas se o arquivo não existir
            writer.writerow(row)

        self.logg.info(f"Métricas salvas no arquivo CSV '{csv_file}'.")
        self.logg.info(f"Integridade dos dados: {integridade}")
        self.logg.info(f"Bytes perdidos: {bytes_lost}")

    def run(self):
        # Inicia a comunicação com o servidor e recebe o arquivo
        self._init_logging()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # Conectar ao servidor TCP na porta especificada
                sock.connect((self.host, self.port))
                self.logg.info("Conectado ao servidor.")

                # Enviar o nome do arquivo e o tamanho do buffer para o servidor
                sock.sendall(f"{self.file_name},{self.buffer_size}".encode())
                self.logg.info(f"Solicitação do arquivo '{self.file_name}' enviada.")

                # Aguardar a confirmação do servidor
                if sock.recv(1024) != b"READY":
                    self.logg.error("O servidor não está pronto para enviar o arquivo.")
                    return

                # Receber os dados do arquivo
                total_received = 0
                packet_count = 0
                start_time = time.time()  # Marca o tempo de início da transferência

                while True:
                    # Recebe os dados do servidor em blocos de tamanho buffer_size
                    data = sock.recv(self.buffer_size)
                    if not data:
                        break  # Fim da transferência
                    total_received += len(data)
                    packet_count += 1

                    if self.verbose:
                        self.logg.debug(
                            f"Pacote {packet_count}: {len(data)} bytes recebidos."
                        )

                # Calcula o tempo total decorrido e a taxa de transferência
                elapsed_time = time.time() - start_time
                throughput = total_received / elapsed_time / (1024 * 1024)  # MB/s

                # Logar as métricas no CSV
                self._log_metrics_to_csv(
                    total_received,
                    elapsed_time,
                    packet_count,
                    throughput,
                    total_received,
                )

                self.logg.info(
                    f"Arquivo recebido em {elapsed_time:.2f} segundos. Taxa: {throughput:.2f} MB/s"
                )

            except Exception as e:
                # Captura e loga qualquer erro que ocorrer durante a execução
                self.logg.error(f"Erro: {e}")
            finally:
                # Garante que a conexão será encerrada corretamente
                self.logg.info("Conexão encerrada.")


def parse_args(args):
    # Função para analisar os argumentos da linha de comando
    import argparse

    parser = argparse.ArgumentParser(description="Cliente TCP - Recepção de Arquivo")
    parser.add_argument(
        "--host", required=True, type=str, help="Endereço IP do servidor"
    )
    parser.add_argument(
        "--port", required=True, type=int, help="Número da porta do servidor"
    )
    parser.add_argument(
        "--file", required=True, type=str, help="Nome do arquivo a ser solicitado"
    )
    parser.add_argument("--buffer", required=True, type=int, help="Tamanho do buffer")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Ativar log detalhado dos pacotes"
    )
    return parser.parse_args(args)


def main():
    # Função principal que inicializa o cliente com os argumentos fornecidos
    args = parse_args(sys.argv[1:])
    client = Client(args.host, args.port, args.buffer, args.file, args.verbose)
    client.run()


if __name__ == "__main__":
    main()
