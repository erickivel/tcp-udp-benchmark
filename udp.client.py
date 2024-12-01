import socket
import logging
import sys
import time
import csv
import os


class Client:
    def __init__(self, host, port, buffer_size, file_name, verbose):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.file_name = file_name
        self.verbose = verbose
        self.logg = logging.getLogger("CLIENTE_UDP")

    def _init_logging(self):
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level)
        self.logg.info(f"Cliente UDP conectando a {self.host}:{self.port}")

    def _log_metrics_to_csv(
        self, total_received, elapsed_time, packet_count, throughput, actual_file_size
    ):
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

                sock.sendto(
                    f"{self.file_name},{self.buffer_size}".encode(),
                    (self.host, self.port),
                )

                total_received = 0
                packet_count = 0
                start_time = time.time()

                sock.settimeout(
                    2
                )  # Definindo um tempo limite para a recepção de pacotes
                while True:
                    try:
                        # Receber dados do servidor
                        data, _ = sock.recvfrom(self.buffer_size)
                        if not data:
                            break
                        total_received += len(data)
                        packet_count += 1

                        if self.verbose:
                            self.logg.debug(
                                f"Pacote {packet_count}: {len(data)} bytes recebidos."
                            )
                    except socket.timeout:
                        self.logg.info("Timeout atingido. Transferência concluída.")
                        break

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
    args = parse_args(sys.argv[1:])
    client = Client(args.host, args.port, args.buffer, args.file, args.verbose)
    client.run()


if __name__ == "__main__":
    main()
