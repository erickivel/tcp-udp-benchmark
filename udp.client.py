import socket
import logging
import sys
import time
import io


class Client:
    """
    Inicializa o cliente UDP com as configurações fornecidas.

    @param host: Endereço IP do servidor.
    @param port: Porta do servidor.
    @param output_file: Caminho do arquivo para salvar os dados recebidos.
    @param verbose: Se verdadeiro, ativa o log detalhado.
    """

    def __init__(self, host, port, output_file, verbose):
        self.host = host
        self.port = port
        self.output_file = output_file
        self.verbose = verbose
        self.logg = logging.getLogger("CLIENTE_UDP")

    def _init_logging(self):
        """
        Configura o sistema de logging com base no nível de verbosidade.
        """
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level)
        self.logg.info(
            f"Cliente UDP inicializado para conectar a {self.host}:{self.port}"
        )

    """
    Inicia a execução do cliente UDP: envia o sinal de prontidão e recebe o arquivo.
    """

    def run(self):
        self._init_logging()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                # Enviar sinal de prontidão ao servidor
                sock.sendto(b"READY", (self.host, self.port))
                self.logg.info("Sinal de prontidão enviado ao servidor.")

                start_time = time.time()  # Marca o tempo de início da recepção
                total_received = 0
                packet_count = 0
                with open(self.output_file, "wb") as file:
                    sock.settimeout(2)  # Define timeout para evitar espera infinita
                    while True:
                        try:
                            data, _ = sock.recvfrom(io.DEFAULT_BUFFER_SIZE)
                            if not data:
                                break  # Fim do arquivo
                            file.write(data)
                            packet_count += 1
                            total_received += len(data)
                            if self.verbose:
                                self.logg.debug(
                                    f"Pacote {packet_count} recebido, tamanho: {len(data)} bytes"
                                )
                        except socket.timeout:
                            # Timeout usado para detectar fim do arquivo em UDP
                            self.logg.info(
                                "Sem mais dados do servidor. Transferência concluída."
                            )
                            break

                elapsed_time = time.time() - start_time  # Tempo total da transferência
                throughput = (
                    total_received / elapsed_time / (1024 * 1024)
                )  # Taxa de transferência em MB/s

                self.logg.info(
                    f"Arquivo recebido com sucesso em {elapsed_time:.2f} segundos."
                )
                self.logg.info(
                    f"Tamanho total: {total_received} bytes em {packet_count} pacotes."
                )
                self.logg.info(f"Taxa de transferência: {throughput:.2f} MB/s")
                self.logg.info(f"Arquivo salvo como '{self.output_file}'.")

            except Exception as e:
                self.logg.error(f"Erro: {e}")
            finally:
                self.logg.info("Execução do cliente finalizada.")


"""
Analisa os argumentos da linha de comando.

@param args: Lista de argumentos passados pela linha de comando.
@return: Objeto contendo os valores dos argumentos.
"""


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
        "--output",
        required=True,
        type=str,
        help="Caminho para salvar o arquivo recebido",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Ativar log detalhado dos pacotes"
    )
    return parser.parse_args(args)


"""
Função principal: Inicializa o cliente com base nos argumentos da linha de comando e executa.
"""


def main():
    args = parse_args(sys.argv[1:])
    client = Client(args.host, args.port, args.output, args.verbose)
    client.run()


if __name__ == "__main__":
    main()
