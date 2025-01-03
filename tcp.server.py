import socket
import logging
import sys
import time
import os


class Server:
    def __init__(self, host, port, verbose):
        # Inicializa o servidor com os parâmetros fornecidos
        # @host - endereço IP do servidor
        # @port - número da porta onde o servidor estará ouvindo conexões
        # @verbose - nível de detalhamento do log (True para log detalhado)
        self.host = host
        self.port = port
        self.verbose = verbose
        self.logg = logging.getLogger("SERVIDOR_TCP")

    def _init_logging(self):
        # Configura o sistema de logging com o nível adequado
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level)
        self.logg.info(f"Servidor TCP inicializado em {self.host}:{self.port}.")

    def _handle_client(self, conn):
        try:
            # Recebe informações do cliente: nome do arquivo e tamanho do buffer
            file_info = conn.recv(1024).decode().split(",")
            file_name, buffer_size = file_info[0], int(file_info[1])
            file_path = "send_data/" + file_name  # Caminho do arquivo a ser enviado

            # Verifica se o arquivo existe
            if not os.path.isfile(file_path):
                self.logg.error(f"Arquivo '{file_path}' não encontrado.")
                conn.sendall(b"ERROR: File not found.")
                return

            # Envia confirmação ao cliente informando que o servidor está pronto
            conn.sendall(b"READY")
            self.logg.info(
                f"Preparando para enviar '{file_path}' com buffer de {buffer_size} bytes."
            )

            # Inicia a transferência do arquivo
            start_time = time.time()  # Marca o tempo de início da transferência
            with open(file_path, "rb") as file:
                packet_count = 0
                total_sent = 0

                # Lê e envia o arquivo em blocos do tamanho do buffer especificado
                while chunk := file.read(buffer_size):
                    conn.sendall(chunk)
                    packet_count += 1
                    total_sent += len(chunk)

                    if self.verbose:
                        self.logg.debug(
                            f"Pacote {packet_count} enviado, tamanho: {len(chunk)} bytes"
                        )

            # Calcula o tempo total decorrido e a taxa de transferência
            elapsed_time = time.time() - start_time
            throughput = total_sent / elapsed_time / (1024 * 1024)  # MB/s
            self.logg.info(
                f"Arquivo '{file_path}' enviado em {elapsed_time:.2f} segundos. Taxa: {throughput:.2f} MB/s"
            )

        except Exception as e:
            # Captura e loga qualquer erro ocorrido durante a transferência
            self.logg.error(f"Erro ao enviar o arquivo: {e}")
        finally:
            # Garante que a conexão com o cliente será encerrada corretamente
            conn.close()
            self.logg.info("Conexão encerrada.")

    def run(self):
        # Inicia o servidor TCP e aguarda conexões de clientes
        self._init_logging()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # Liga o servidor ao endereço e porta especificados
                sock.bind((self.host, self.port))
                sock.listen(5)  # Define o número máximo de conexões em espera
                self.logg.info(f"Servidor ouvindo em {self.host}:{self.port}")

                while True:
                    conn, addr = sock.accept()  # Aguarda uma nova conexão
                    self.logg.info(f"Conexão aceita de {addr}")
                    self._handle_client(conn)

            except Exception as e:
                # Captura e loga qualquer erro ocorrido durante a execução do servidor
                self.logg.error(f"Erro no servidor: {e}")


def parse_args(args):
    # Função para analisar os argumentos da linha de comando
    import argparse

    parser = argparse.ArgumentParser(description="Servidor TCP - Envio de Arquivo")
    parser.add_argument("--host", required=True, type=str, help="Endereço IP do host")
    parser.add_argument("--port", required=True, type=int, help="Número da porta")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Ativar log detalhado dos pacotes"
    )
    return parser.parse_args(args)


def main():
    # Função principal que inicializa o servidor com os argumentos fornecidos
    args = parse_args(sys.argv[1:])
    server = Server(args.host, args.port, args.verbose)
    server.run()


if __name__ == "__main__":
    main()
