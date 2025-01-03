import socket
import logging
import sys
import time
import os


class Server:
    def __init__(self, host, port, verbose):
        # Inicializa o servidor com os parâmetros fornecidos
        # @host - endereço IP do servidor
        # @port - número da porta onde o servidor vai escutar
        # @verbose - nível de detalhamento do log (True para log detalhado)
        self.host = host
        self.port = port
        self.verbose = verbose
        self.logg = logging.getLogger("SERVIDOR_UDP")

    def _init_logging(self):
        # Configura o sistema de logging com o nível adequado
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level)
        self.logg.info(f"Servidor UDP inicializado em {self.host}:{self.port}.")

    def _send_file(self, sock, client_addr):
        # Envia um arquivo para o cliente especificado
        # @sock - socket utilizado para a comunicação
        # @client_addr - endereço do cliente que receberá o arquivo
        try:
            # Recebe o nome do arquivo e o tamanho do buffer do cliente
            data, _ = sock.recvfrom(1024)
            file_info = data.decode().split(",")
            print("File info", file_info)
            file_name, buffer_size = file_info[0], int(file_info[1])

            # Caminho do arquivo a ser enviado
            file_name = "send_data/" + file_name

            # Verifica se o arquivo existe
            if not os.path.isfile(file_name):
                self.logg.error(f"Arquivo '{file_name}' não encontrado.")
                return

            self.logg.info(
                f"Preparando para enviar '{file_name}' com buffer de {buffer_size} bytes."
            )

            # Inicia a transferência do arquivo
            start_time = time.time()
            packet_count = 0
            total_sent = 0

            with open(file_name, "rb") as file:
                while chunk := file.read(buffer_size):
                    # Envia o arquivo em pacotes do tamanho do buffer
                    sock.sendto(chunk, client_addr)
                    packet_count += 1
                    total_sent += len(chunk)
                    if self.verbose:
                        self.logg.debug(
                            f"Pacote {packet_count} enviado, tamanho: {len(chunk)} bytes"
                        )

            # Calcula o tempo total de transferência e a taxa de transferência
            elapsed_time = time.time() - start_time
            throughput = total_sent / elapsed_time / (1024 * 1024)  # Converte para MB/s
            self.logg.info(
                f"Arquivo '{file_name}' enviado em {elapsed_time:.2f} segundos. Taxa: {throughput:.2f} MB/s"
            )
        except Exception as e:
            self.logg.error(f"Erro ao enviar o arquivo: {e}")

    def run(self):
        # Inicia o servidor e aguarda conexões de clientes
        self._init_logging()
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            try:
                # Associa o socket ao endereço e porta especificados
                sock.bind((self.host, self.port))
                self.logg.info(f"Servidor ouvindo em {self.host}:{self.port}")

                while True:
                    # Aguarda um sinal de prontidão do cliente
                    data, client_addr = sock.recvfrom(1024)
                    if data != b"READY":
                        self.logg.error("Sinal de prontidão inválido do cliente.")
                        continue

                    self.logg.info(
                        f"Sinal de prontidão recebido de {client_addr}. Iniciando transferência do arquivo."
                    )

                    # Envia confirmação de prontidão para o cliente
                    sock.sendto(b"READY", client_addr)

                    # Inicia o envio do arquivo
                    self._send_file(sock, client_addr)

            except Exception as e:
                self.logg.error(f"Erro no servidor: {e}")
            finally:
                self.logg.info("Execução do servidor finalizada.")


def parse_args(args):
    # Função para analisar os argumentos da linha de comando
    import argparse

    parser = argparse.ArgumentParser(description="Servidor UDP - Envio de Arquivo")
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
