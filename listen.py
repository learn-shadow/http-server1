# ::NOTE: (Most Important)*
# ------------------------------------------------------------------------------------------------------------------------------- #
# - This file is responsible for the code required for starting a server ! All its utilized methods are already documented in --- #
# --------------------------------------------------- file HelpListner ! -------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------- IMPORTING NECESSARY MODULES ------------------------------------------------- #
import ctypes
from help_me_durdana import HelpListener
from ctype_socket import SocketDeclaration



# ------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------ SETTING UP THE CLASS RESPONSIBLE FOR SETTING UP THE SERVER FOR LISTENING ----------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #
class StartListening(HelpListener):
    def __init__(self) -> None:
        super().__init__()

    def start_listner(self) -> int | Exception:
        """
            -- This method returns the file descriptor of the socket that gets binded and is used for the system for listening ;
        """
        try:
            new_socket = self.new_socket_object(self.ipv4_connection, self.sock_stream, self.tcp_protocol)

            # ---------- Binding the socket to the address and calling its only method to poppulate the Schema ---------------- #
            socket = SocketDeclaration()
            socket.configure_socket_instance(self.ipv4_connection, self.available_port, bytes(self.host_address))

            # ---------------------- Binding the socket to the address and starting the server -------------------------------- #
            self.bind_socket(new_socket, ctypes.byref(socket), ctypes.sizeof(socket))
            self.start_listening(new_socket, self.basic_backlog)

            return new_socket
        
        except Exception as e:
            raise Exception(f"Unable to setup Listening Server : {e}".title())




if __name__ == '__main__':
    pass