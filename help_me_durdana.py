# ::NOTE: (Most Important)*
# ------------------------------------------------------------------------------------------------------------------------------- #
# - Don't take it serious ; I was just unable to think of a good name for this file ; well it holds the code is responsible ----- #
# - for creating a new socket, binding the socket to the server and then making the server listen at an address. All of these --- #
# -------------------------- methods are very important to setup the server even for host side ; -------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #

"""
    -- workflow for these methods goes like this ;
        1 - A new socket needs to be created for every new connection requiring information like connection type, stream type and
            the protocol.
        2 - Once the socket is created we need to bind that socket to a given address ;
        3 - at last we can just set our server to listen at given address
"""



# ------------------------------------------------- IMPORTING NECESSARY MODULES ------------------------------------------------- #
import os
import ctypes
from accept import AcceptConnection
from config import ConfigurationFetcher



# ------------------------------------------------------------------------------------------------------------------------------- #
# -------------------- SETTING UP THE CLASS RESPONSIBLE FOR HAVING METHODS REQUIRED TO SETUP A SERVER --------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #
class HelpListener(AcceptConnection, ConfigurationFetcher):
    """
        -- AcceptConnection class is used because i need the libc_object ; Well i can create one but just to avoid using the code
            that already been written i preffered to use Inheritance !
    """
    def __init__(self):
        AcceptConnection.__init__(self)
        ConfigurationFetcher.__init__(self)

        self.basic_backlog : int = 5
        self.standard_backlog : int = 20
        self.hard_backlog : int = 40
        self.host_ip_address : str = '.'.join(str(self.host_address)[1 : -1].split(", "))


    def new_socket_object(self, connection_type, stream_type, protocol_type) -> object | Exception:
        """
            -- Creating of new socket ; this is necessary for every new connection ! Make sure you provide the
                correct sock_stream and protocol type for a successfull connection ! like sock_stream with tcp
                protocol !
        """
        try:
            new_socket = self.libc_object.socket(connection_type, stream_type, protocol_type)
            if new_socket < 0:
                raise Exception(f"Unable to solve Socket : {os.strerror(ctypes.get_errno())}")
            
            print(f"new socket gets created successfully : File Descriptor = {new_socket}".title())
            return new_socket
        
        except ConnectionError:
            raise ConnectionError("Connection error, Cannot create socket")
        
        except Exception as e:
            raise Exception(f"Could not create new socket : {e}")

    
    def bind_socket(self, socket_object, instance_reference, instance_size) -> Exception:
        """
            -- binding socket to the given address ; For this method the socket address is required instead of the
                actual values !
        """
        try:
            result = self.libc_object.bind(socket_object, instance_reference, instance_size)
            if result < 0:
                raise Exception(f"Unable to Bind Socket to address : {os.strerror(ctypes.get_errno())}")
            
            print(f"Socket Gets Bind with Given Address : IP = {self.host_ip_address}, port = {self.available_port}".title())

        except ConnectionError:
            raise ConnectionError("Connection error, Cannot bind socket")
        
        except Exception as e:
            raise Exception(f"Unable to bind socket: {e}")


    def start_listening(self, socket_object, backlog) -> Exception:
        """
            -- starting a server at given address ; A basic backlog is provided for this server so at max it can hold upto
                a very limited amount of requests !
        """
        try:
            listen_result : int = self.libc_object.listen(socket_object, backlog)
            if listen_result < 0:
                raise Exception(f"Unable to start listening : {os.strerror(ctypes.get_errno())}")

        except ConnectionError:
            raise ConnectionError("Connection error, Cannot listen on socket")
        
        except Exception as e:
            raise Exception(f"Unable to Listen... {e}")
        


if __name__ == '__main__':
    pass