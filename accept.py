# ::NOTE: (Most Important)*
# ------------------------------------------------------------------------------------------------------------------------------- #
# - This file holds the code section that is used to accept the upcomming connections to the server and is used in listen.py ---- #
# - file. Loading the libc library is carried out in this below class constructor instead of the StartListening class. to ------- #
# - the connection we need libc object. As this code was seperated from file listen.py it was necessary to include this loading - #
# - process here. This Class gets inherited in StartListening doing providing the same libc object required to set u the server - #
# ---------------------------------------------------- for listening ------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------- #


"""
    -- Workflow to use this class constructor and methods goes like this:
        1 - Loading main libc_library here that is utilized in listen.py and listen.py main class gets utilized in connection.py
            effectively providing the libc object for different files ; As this is a local project just to get a slight
            understanding of how system behaves internally we can avoid using the same code in subsequent Files.

            1.1 - The libc_object gets to the listen.py by after the inherited use in help_me_durdana.py file !

        2 - The libc_object from this constructor first gets utilized by listen.py to create a socket and then connection.py
            to create the host side socket !
        3 - accept_connection method is used to accept upcoming connections to the listening server
"""


# ------------------------------------------------- IMPORTING NECESSARY MODULES ------------------------------------------------- #
import os
import struct
import ctypes
from ctype_socket import SocketDeclaration


# ------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------- SETTING UP THE CLASS RESPONSIBLE FOR ACCEPTNING AN UPCOMING CONNECTION ------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------- #
class AcceptConnection:
    def __init__(self):
        """
            -- NOTE: loading libc library for socket creation ! As mentioned before this shouldn't be done here but in a local
                project to understand how system works we can fuck around !
        """
        self.libc_object : ctypes = ctypes.CDLL("libc.so.6", use_errno = True)
        self.acceptance_message : str = b"You are connected to the server successfully !"


    def accept_connection(self, socket_object) -> object | Exception:
        """
            -- This method tries to accept the upcoming connection request at the bounded port and IP. It retreives the
                host request configuration like port and IP using SocketDeclaration schema and return then after trying to
                accepting the connection.
        """
        try:
            # ---------------------------------------- Getting upcoming request Schema ---------------------------------------- #
            client_address = SocketDeclaration()
            client_address_size = ctypes.c_int(ctypes.sizeof(client_address))
            client_address_pointer = ctypes.pointer(client_address)

            client_socket = self.libc_object.accept(socket_object, client_address_pointer, ctypes.byref(client_address_size))
            if client_socket < 0:
                raise Exception(f"Unable to accept incoming connection : {os.strerror(ctypes.get_errno())}")
            
            acceptance_message = self.send_acceptance_message(client_socket)

            client_ip_address = struct.unpack('BBBB', bytes(client_address.sin_addr))
            client_ip_address = '.'.join(str(byte) for byte in client_ip_address)
            return client_socket, client_ip_address, client_address.sin_port, acceptance_message
        
        except ConnectionError:
            raise ConnectionError("Connection error, Cannot accept incoming connections")
        
        except Exception as e:
            raise Exception(f"Unable to accept incoming connections : {e}")
    

    def send_acceptance_message(self, client_socket) -> Exception | int:
        """
            -- Sending Acceptance Message to the requesting host ! This method is called accept_connection method so avoid
                remembering we have to call this in listen.py or not !
        """
        send_result = self.libc_object.send(client_socket, self.acceptance_message, len(self.acceptance_message), 0)
        if send_result < 0:
            raise Exception(f"Unable to send message to client : {os.strerror(ctypes.get_errno())}")
        
        return send_result
    

    def display_server_side_logs(self, client_ip_address, client_port, acceptance_message_length) -> Exception:
        """
            -- this method is used to render logs at server terminal so listen.py file kind of looks cool ! There is no other
                reason to define this method here !
        """
        try:
            print(f"::Accepted connection from client: IP = {client_ip_address}, Port = {client_port}".title())
            print(f"::Sent message to client: IP = {client_ip_address}, Port = {client_port}, Message = {self.acceptance_message.decode('utf-8')}, length = {acceptance_message_length}")

        except Exception as e:
            raise Exception(f"Unable to display server side logs: {e}")



if __name__ == '__main__':
    pass