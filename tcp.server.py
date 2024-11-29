import socket
import logging
import sys
import time
import io


class Server:
    def __init__(self, host, port, file_path, verbose):
        self.host = host
        self.port = port
        self.file_path = file_path
        self.verbose = verbose
        self.logg = logging.getLogger("tcp_server_file_sender")

    def _init_logging(self):
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(level=level)
        self.logg.info(f"TCP server initialized on {self.host}:{self.port}")

    def run(self):
        self._init_logging()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((self.host, self.port))
                sock.listen(1)
                self.logg.info(f"Server listening on {self.host}:{self.port}")

                conn, addr = sock.accept()
                self.logg.info(f"Connection accepted from {addr}")
                self._handle_client(conn)
            except Exception as e:
                self.logg.error(f"Server error: {e}")
            finally:
                self.logg.info("Server execution finished.")

    def _handle_client(self, conn):
        try:
            readiness = conn.recv(1024)
            if readiness != b"READY":
                self.logg.error("Invalid readiness signal from client.")
                return

            self.logg.info("Readiness signal received. Starting file transfer.")
            start_time = time.time()

            with open(self.file_path, "rb") as file:
                packet_count = 0
                total_sent = 0
                while chunk := file.read(
                    io.DEFAULT_BUFFER_SIZE
                ):  # Send file in 8KB chunks
                    conn.sendall(chunk)
                    packet_count += 1
                    total_sent += len(chunk)
                    if self.verbose:
                        self.logg.debug(
                            f"Sent packet {packet_count}, size: {len(chunk)} bytes"
                        )

            elapsed_time = time.time() - start_time
            throughput = total_sent / elapsed_time / (1024 * 1024)

            self.logg.info(
                f"File '{self.file_path}' sent successfully in {elapsed_time:.2f} seconds."
            )
            self.logg.info(
                f"Total packets: {packet_count}, Total data: {total_sent} bytes."
            )
            self.logg.info(f"Throughput: {throughput:.2f} MB/s")

        except Exception as e:
            self.logg.error(f"Error while sending file: {e}")
        finally:
            conn.close()
            self.logg.info("Connection closed. Server shutting down.")


def parse_args(args):
    import argparse

    parser = argparse.ArgumentParser(description="TCP Server - File Sender")
    parser.add_argument("--host", required=True, type=str, help="Host IP address")
    parser.add_argument("--port", required=True, type=int, help="Port number")
    parser.add_argument(
        "--file", required=True, type=str, help="Path to the file to send"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable detailed packet logging"
    )
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    server = Server(args.host, args.port, args.file, args.verbose)
    server.run()


if __name__ == "__main__":
    main()
