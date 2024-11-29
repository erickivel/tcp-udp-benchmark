import socket
import logging
import sys
import time
import io


class Server:
    """
    Inicializa o servidor TCP com as configurações fornecidas.

    @param host: Endereço IP do servidor.
    @param port: Porta do servidor.
    @param file_path: Caminho do arquivo que será enviado ao cliente.
    @param verbose: Se verdadeiro, ativa o log detalhado.
    """

    def __init__(self, host, port, file_path, verbose):
        self.host = host
        self.port = port
        self.file_path = file_path
        self.verbose = verbose
        self.logg = logging.getLogger("SERVIDOR_TCP")

    """
    Configura o sistema de logging com base no nível de verbosidade.
    """

    def _init_logging(self):
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level)
        self.logg.info(f"Servidor TCP inicializado em {self.host}:{self.port}")

    """
    Lida com a comunicação com o cliente, incluindo o envio do arquivo.

    @param conn: Conexão estabelecida com o cliente.
    """

    def _handle_client(self, conn):
        try:
            # Espera o sinal de prontidão do cliente
            readiness = conn.recv(1024)
            if readiness != b"READY":
                self.logg.error("Sinal de prontidão inválido do cliente.")
                return

            self.logg.info(
                "Sinal de prontidão recebido. Iniciando transferência do arquivo."
            )
            start_time = time.time()  # Marca o tempo de início da transmissão

            with open(self.file_path, "rb") as file:
                packet_count = 0
                total_sent = 0
                while chunk := file.read(io.DEFAULT_BUFFER_SIZE):
                    conn.sendall(chunk)
                    packet_count += 1
                    total_sent += len(chunk)
                    if self.verbose:
                        self.logg.debug(
                            f"Pacote {packet_count} enviado, tamanho: {len(chunk)} bytes"
                        )

            # Calcula o tempo total de envio e a taxa de transferência
            elapsed_time = time.time() - start_time
            throughput = total_sent / elapsed_time / (1024 * 1024)

            self.logg.info(
                f"Arquivo '{self.file_path}' enviado com sucesso em {elapsed_time:.2f} segundos."
            )
            self.logg.info(
                f"Total de pacotes: {packet_count}, Total de dados: {total_sent} bytes."
            )
            self.logg.info(f"Taxa de transferência: {throughput:.2f} MB/s")

        except Exception as e:
            self.logg.error(f"Erro ao enviar o arquivo: {e}")
        finally:
            conn.close()  # Fecha a conexão com o cliente
            self.logg.info("Conexão encerrada. Servidor desligando.")

    """
    Inicia a execução do servidor TCP: espera por uma conexão e gerencia o envio do arquivo.
    """

    def run(self):
        self._init_logging()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((self.host, self.port))
                sock.listen(1)
                self.logg.info(f"Servidor ouvindo em {self.host}:{self.port}")

                conn, addr = sock.accept()
                self.logg.info(f"Conexão aceita de {addr}")
                self._handle_client(conn)  # Lida com a transferência do arquivo
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

    parser = argparse.ArgumentParser(description="Servidor TCP - Envio de Arquivo")
    parser.add_argument("--host", required=True, type=str, help="Endereço IP do host")
    parser.add_argument("--port", required=True, type=int, help="Número da porta")
    parser.add_argument(
        "--file", required=True, type=str, help="Caminho do arquivo a ser enviado"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Ativar log detalhado dos pacotes"
    )
    return parser.parse_args(args)


"""
Função principal: Inicializa o servidor com base nos argumentos da linha de comando e executa.
"""


def main():
    args = parse_args(sys.argv[1:])
    server = Server(args.host, args.port, args.file, args.verbose)
    server.run()


if __name__ == "__main__":
    main()
