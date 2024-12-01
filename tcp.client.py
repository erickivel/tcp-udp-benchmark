import socket
import logging
import sys
import time
import csv
import os


class Client:
    def __init__(self, host, port, output_file, buffer_size, file_name, verbose):
        self.host = host
        self.port = port
        self.output_file = output_file
        self.buffer_size = buffer_size
        self.file_name = file_name
        self.verbose = verbose
        self.logg = logging.getLogger("CLIENTE_TCP")

    def _init_logging(self):
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level)
        self.logg.info(f"Cliente TCP conectando a {self.host}:{self.port}")

    def _log_metrics_to_csv(
        self, total_received, elapsed_time, packet_count, throughput, actual_file_size
    ):
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

        # Escrever no CSV
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
        self._init_logging()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((self.host, self.port))
                self.logg.info("Conectado ao servidor.")

                # Enviar nome do arquivo e buffer size para o servidor
                sock.sendall(f"{self.file_name},{self.buffer_size}".encode())

                # Aguardar a confirmação do servidor
                if sock.recv(1024) != b"READY":
                    self.logg.error("O servidor não está pronto.")
                    return

                # Receber os dados do arquivo
                total_received = 0
                packet_count = 0
                start_time = time.time()

                with open(self.output_file, "wb") as file:
                    while True:
                        data = sock.recv(self.buffer_size)
                        if not data:
                            break
                        file.write(data)
                        total_received += len(data)
                        packet_count += 1
                        if self.verbose:
                            self.logg.debug(
                                f"Pacote {packet_count}: {len(data)} bytes recebidos."
                            )

                elapsed_time = time.time() - start_time
                throughput = total_received / elapsed_time / (1024 * 1024)  # MB/s
                actual_file_size = os.path.getsize(self.output_file)

                # Logar as métricas no CSV
                self._log_metrics_to_csv(
                    total_received,
                    elapsed_time,
                    packet_count,
                    throughput,
                    actual_file_size,
                )

                self.logg.info(
                    f"Arquivo recebido em {elapsed_time:.2f} segundos. Taxa: {throughput:.2f} MB/s"
                )

            except Exception as e:
                self.logg.error(f"Erro: {e}")
            finally:
                self.logg.info("Conexão encerrada.")


def parse_args(args):
    import argparse

    parser = argparse.ArgumentParser(description="Cliente TCP - Recepção de Arquivo")
    parser.add_argument(
        "--host", required=True, type=str, help="Endereço IP do servidor"
    )
    parser.add_argument(
        "--port", required=True, type=int, help="Número da porta do servidor"
    )
    parser.add_argument(
        "--output",
        required=True,
        type=str,
        help="Caminho para salvar o arquivo recebido",
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
    args = parse_args(sys.argv[1:])
    client = Client(
        args.host, args.port, args.output, args.buffer, args.file, args.verbose
    )
    client.run()


if __name__ == "__main__":
    main()
