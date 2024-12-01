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
        self.logg = logging.getLogger("CLIENTE_UDP")

    def _init_logging(self):
        # Configura o sistema de logging com o nível adequado
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level)
        self.logg.info(f"Cliente UDP conectando a {self.host}:{self.port}")

    def _log_metrics_to_csv(
        self, total_received, elapsed_time, packet_count, throughput, actual_file_size
    ):
        # Salva métricas da transferência em um arquivo CSV
        # @total_received - total de bytes recebidos durante a transferência
        # @elapsed_time - tempo total decorrido para a transferência
        # @packet_count - número de pacotes recebidos
        # @throughput - taxa de transferência em MB/s
        # @actual_file_size - tamanho esperado do arquivo
        csv_file = "metricas_udp.csv"
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

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                # Enviar o sinal "READY" para o servidor
                sock.sendto(b"READY", (self.host, self.port))
                self.logg.info("Sinal de prontidão (READY) enviado ao servidor.")

                # Aguardar resposta do servidor
                response, _ = sock.recvfrom(self.buffer_size)
                if response != b"READY":
                    self.logg.error("O servidor não respondeu com 'READY'.")
                    return

                self.logg.info("Servidor está pronto para enviar o arquivo.")

                # Enviar informações do arquivo e buffer ao servidor
                sock.sendto(
                    f"{self.file_name},{self.buffer_size}".encode(),
                    (self.host, self.port),
                )

                total_received = 0
                packet_count = 0
                start_time = time.time()  # Marca o tempo de início da transferência

                sock.settimeout(
                    2
                )  # Define um tempo limite (timeout) para a recepção de pacotes
                while True:
                    try:
                        # Receber dados do servidor
                        data, _ = sock.recvfrom(self.buffer_size)
                        if not data:
                            break  # Fim da transferência
                        total_received += len(data)
                        packet_count += 1

                        if self.verbose:
                            self.logg.debug(
                                f"Pacote {packet_count}: {len(data)} bytes recebidos."
                            )
                    except socket.timeout:
                        # Se o timeout for atingido, a transferência é considerada concluída
                        self.logg.info("Timeout atingido. Transferência concluída.")
                        break

                # Calcula o tempo total decorrido e a taxa de transferência
                elapsed_time = time.time() - start_time
                throughput = total_received / elapsed_time / (1024 * 1024)  # MB/s

                # Exibir informações de métricas
                self.logg.info(f"Arquivo recebido em {elapsed_time:.2f} segundos.")
                self.logg.info(f"Tamanho total recebido: {total_received} bytes.")
                self.logg.info(f"Taxa de transferência: {throughput:.2f} MB/s.")

                # Registrar as métricas no arquivo CSV
                self._log_metrics_to_csv(
                    total_received,
                    elapsed_time,
                    packet_count,
                    throughput,
                    total_received,
                )

            except Exception as e:
                self.logg.error(f"Erro: {e}")
            finally:
                self.logg.info("Execução do cliente finalizada.")


def parse_args(args):
    # Função para analisar os argumentos da linha de comando
    import argparse

    parser = argparse.ArgumentParser(description="Cliente UDP - Recepção de Arquivo")
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
