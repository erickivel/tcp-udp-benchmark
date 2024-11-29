import socket
import logging
import sys
import time
import io


class Server:
    """
    Inicializa o servidor UDP com as configurações fornecidas.

    @param host: Endereço IP do servidor.
    @param port: Porta na qual o servidor irá escutar.
    @param file_path: Caminho do arquivo a ser enviado.
    @param verbose: Se verdadeiro, ativa o log detalhado.
    """

    def __init__(self, host, port, file_path, verbose):
        self.host = host
        self.port = port
        self.file_path = file_path
        self.verbose = verbose
        self.logg = logging.getLogger("SERVIDOR_UDP")

    """
    Configura o sistema de logging com base no nível de verbosidade.
    """

    def _init_logging(self):
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level)
        self.logg.info(f"Servidor UDP inicializado em {self.host}:{self.port}")

    """
    Envia o arquivo para o cliente especificado.

    @param sock: Socket UDP utilizado para a comunicação.
    @param client_addr: Endereço do cliente para o qual o arquivo será enviado.
    """

    def _send_file(self, sock, client_addr):
        try:
            start_time = time.time()  # Marca o tempo de início da transferência
            packet_count = 0
            total_sent = 0

            with open(self.file_path, "rb") as file:
                while chunk := file.read(8196):
                    sock.sendto(chunk, client_addr)
                    packet_count += 1
                    total_sent += len(chunk)
                    if self.verbose:
                        self.logg.debug(
                            f"Pacote {packet_count} enviado, tamanho: {len(chunk)} bytes"
                        )

            elapsed_time = (
                time.time() - start_time
            )  # Calcula o tempo total da transferência
            throughput = (
                total_sent / elapsed_time / (1024 * 1024)
            )  # Taxa de transferência em MB/s

            self.logg.info(
                f"Arquivo '{self.file_path}' enviado com sucesso em {elapsed_time:.2f} segundos."
            )
            self.logg.info(
                f"Total de pacotes: {packet_count}, Total de dados: {total_sent} bytes."
            )
            self.logg.info(f"Taxa de transferência: {throughput:.2f} MB/s")

        except Exception as e:
            self.logg.error(f"Erro ao enviar arquivo: {e}")

    """
    Inicia o servidor UDP, aguarda a conexão do cliente e gerencia a transferência do arquivo.
    """

    def run(self):
        self._init_logging()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                sock.bind((self.host, self.port))
                self.logg.info(f"Servidor ouvindo em {self.host}:{self.port}")

                # Aguarda o sinal de prontidão do cliente
                data, client_addr = sock.recvfrom(1024)
                if data != b"READY":
                    self.logg.error("Sinal de prontidão inválido do cliente.")
                    return

                self.logg.info(
                    f"Sinal de prontidão recebido de {client_addr}. Iniciando transferência do arquivo."
                )
                self._send_file(sock, client_addr)

            except Exception as e:
                self.logg.error(f"Erro no servidor: {e}")
            finally:
                self.logg.info("Execução do servidor finalizada.")


"""
Analisa os argumentos da linha de comando.

@param args: Lista de argumentos passados pela linha de comando.
@return: Objeto contendo os valores dos argumentos.
"""


def parse_args(args):
    import argparse

    parser = argparse.ArgumentParser(description="Servidor UDP - Envio de Arquivos")
    parser.add_argument("--host", required=True, type=str, help="Endereço IP do host")
    parser.add_argument("--port", required=True, type=int, help="Número da porta")
    parser.add_argument(
        "--file", required=True, type=str, help="Caminho do arquivo a ser enviado"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Habilitar log detalhado de pacotes",
    )
    return parser.parse_args(args)


"""
Função principal: Inicializa o servidor com base nos argumentos da linha de comando.
"""


def main():
    args = parse_args(sys.argv[1:])
    server = Server(args.host, args.port, args.file, args.verbose)
    server.run()


if __name__ == "__main__":
    main()
