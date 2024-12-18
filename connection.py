# ::NOTE: (Most Important)*
# ------------------------------------------------------------------------------------------------------------------------------- #
# - This file includes the code that is required for trying to establish a connection to ther server as a host. This code ------- #
# - heavily depends on the StartListening class responsible for setting up a root server. Definately a more robust way would ---- #
# - be to not use StartListening as a dependency but just for the sake of learning i'm doing so so i can avoid writting same ---- #
# -------------------------------------------------- code is subsequent files ! ------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #

"""
    -- Worflow for establishing a connection to the server includes : 
        1 - Setting up the socket with same credentials the server is lsitening at.
        2 - Binding the socket to the address to establish connection.
        3 - connecting to the server using socket file descriptor
        4 - Expect a message of connection establishment !
"""

# ------------------------------------------------- IMPORTING NECESSARY MODULES ------------------------------------------------- #
import os
import ctypes
from listen import StartListening
from ctype_socket import SocketDeclaration # ------------------ Responsible for socket schema ! --------------------------------- #

# ------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------- SETTING UP THE CLASS RESPONSIBLE FOR ESTABLISHING A CONNECTION TO THE SERVER --------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #
class EstablishConnection(StartListening):
    def __init__(self) -> None:
        """
            -- NOTE: using super() is essential to load all required configuration of the server ; As this code only tries to connect
                to the local server on a machine we can use the same configuration as the listening server defined in the
                configuration File !
        """
        super().__init__()
    

    def connect_to_server(self) -> object | Exception:
        """
            -- NOTE: This is not very optimal way of defineing a connetion responsible method ; Definately I'll use non dependent
                method in production ! (
                    ~ Configuration required to connect having ip, port and connection type is loaded by calling StartListening
                        constructor !
                )

            -- TODO: in production server make this include three key arguments insdted of using instance attributes !
        """
        new_socket, connection_result = self.connection_procedure_call()
        if connection_result < 0:
            raise Exception(f"Unable to connect to server : {os.strerror(ctypes.get_errno())}".title())
        
        print(f"\n-> Connecting to server : IP = {self.host_ip_address}, Port = {self.available_port}".title())
        print(f"::Server Response : {self.receive_response_message(new_socket)}")

        return new_socket
        

    def connection_procedure_call(self) -> int:
        """
            -- method that creates the new socket and try to connect to the server using StartListening methods !
        """
        try:
            new_socket = self.new_socket_object(self.ipv4_connection, self.sock_stream, self.tcp_protocol)

            # ---------- Binding the socket to the address and calling its only method to poppulate the Schema ---------------- #
            socket = SocketDeclaration()
            socket.configure_socket_instance(self.ipv4_connection, self.available_port, bytes(self.host_address))

            connection_result = self.libc_object.connect(new_socket, ctypes.byref(socket), ctypes.sizeof(socket))

            return new_socket, connection_result
        
        except ConnectionError:
            raise ConnectionError("Connection error, Cannot connect to server")
        
        except Exception as e:
            raise Exception(f"Unable to connect to server : {e}")


    def receive_response_message(self, new_socket) -> Exception | str:
        """
            -- Trying to get the response from the server ! A maximum size of response buffer can be 1024 bytes !
            -- As an argument this method expects the socket file descriptor where the response will be taken by system
                so we can restore it !
        """
        try:
            message_buffer = ctypes.create_string_buffer(1024)
            recv_result = self.libc_object.recv(new_socket, message_buffer, 1024, 0)
            if recv_result < 0:
                raise Exception(f"Unable to receive message from server : {os.strerror(ctypes.get_errno())}")

            return message_buffer.value.decode('utf-8')

        except ConnectionError:
            raise ConnectionError("Connection error, Cannot connect to server")
        
        except Exception as e:
            raise Exception(f"Unable to receive message from server : {e}")



if __name__ == "__main__":
    pass