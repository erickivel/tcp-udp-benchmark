import socket
import logging
import sys
import time
import io


def receive_file(host, port, output_file, verbose):
    logger = logging.getLogger("tcp_client_file_receiver")
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level)

    logger.info(f"Connecting to {host}:{port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((host, port))
            logger.info("Connected to server.")

            # Send readiness signal to server
            sock.sendall(b"READY")
            logger.info("Sent readiness signal to server.")

            # Receive the file data
            start_time = time.time()
            total_received = 0
            packet_count = 0
            with open(output_file, "wb") as file:
                while True:
                    data = sock.recv(io.DEFAULT_BUFFER_SIZE)
                    if not data:
                        break  # End of file
                    file.write(data)
                    packet_count += 1
                    total_received += len(data)
                    if verbose:
                        logger.debug(
                            f"Received packet {packet_count}, size: {len(data)} bytes"
                        )

            elapsed_time = time.time() - start_time
            throughput = total_received / elapsed_time / (1024 * 1024)

            logger.info(f"File received successfully in {elapsed_time:.2f} seconds.")
            logger.info(
                f"Total size: {total_received} bytes in {packet_count} packets."
            )
            logger.info(f"Throughput: {throughput:.2f} MB/s")
            logger.info(f"File saved as '{output_file}'.")

        except Exception as e:
            logger.error(f"Error: {e}")
        finally:
            sock.close()
            logger.info("Connection closed. Client execution finished.")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="TCP Client - File Receiver")
    parser.add_argument("--host", required=True, type=str, help="Server IP address")
    parser.add_argument("--port", required=True, type=int, help="Server port number")
    parser.add_argument(
        "--output", required=True, type=str, help="Path to save the received file"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable detailed packet logging"
    )

    args = parser.parse_args(sys.argv[1:])
    receive_file(args.host, args.port, args.output, args.verbose)


if __name__ == "__main__":
    main()
