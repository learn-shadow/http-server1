# ::NOTE: (Most Important)*
# ------------------------------------------------------------------------------------------------------------------------------- #
# - This file contains the code of the Ctype Schema of the socket. Libc expects the C programming type objects like int, short -- #
# - and byte. Python has its own generic types that are not compatible with libc methods so we have to use ctype structure of --- #
# -------------------- objects to create HttpServer using only one low leven library libc as base ! ----------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #

"""
    -- Workflow for configuring the socket object attributes goes like this:
        1 - We can use Ipv4 or IPV6 connection for a server ; In libc its type needs to be c_short
        2 - We can use any free port to configure our server for listening with a type of c_uint16
        3 - Ip address bytes are required ; we can use at most 4 bytes that needs to be stored in a form of
            tuple (prefered) or list. there type needs to be c_byte and in c to define an array we must have to
            provide its size also due to its static nature.

        4 -- NOTE: A very interesting line i have included in this project is sin_zero instance in the _fields_ object. you
            can find it last of the object ! After some research i found that sockaddr_in previous Ipv4 address size was
            long and not including this line doesn't confiure the given size of ipv4 to the standard previous size. It only
            kind of like works to ensure compatibility. While figuring out this fact takes up my whole 2 days !

        5 - A method is described in this class that specificaly poppulate this socket CType object with ctype Types !
            Definately we can poppulate in seperate files also across the project but just having a method that takes up some
            raw attributes to configure then according to the standard eliminates the problem of having to wonder what is wrong
            with the configuration if in any file the configuration doesn't match !
"""

# ------------------------------------------------- IMPORTING NECESSARY MODULES ------------------------------------------------- #
import ctypes


# ------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------- SETTING UP THE CLASS RESPONSIBLE FOR ESTABLISHING A CONNECTION TO THE SERVER --------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #
class SocketDeclaration(ctypes.Structure):
    """
        -- Well i tried to change these names to something more fancy but for some reason changing these names leads us to very
            unexpected behavior ! So stick with this initialisation if you are following this code !
    """
    _fields_ = [
        ('sin_family', ctypes.c_short),
        ('sin_port', ctypes.c_uint16),
        ('sin_addr', ctypes.c_byte * 4),
        ('sin_zero', ctypes.c_char * 8)
    ]


    def configure_socket_instance(self, connection_type, port, ip_address_bytes) -> Exception:
        """
            -- Method to poppulate the Socket Object using Standard socket_addr size and CType ! While it is not very
                compulsory to only call this method after initializing the instance ; But is preffered !

            -- NOTE: Kindly do not try to avoid calling this method and being a hero of doing same thing where any mistake
                can cause if not several days but hours to debug ! There is nothing to expect from this method in return !
        """
        try:
            self.sin_family = ctypes.c_short(connection_type)
            self.sin_port = ctypes.c_uint16(port)
            ip_address_bytes = bytes(ip_address_bytes)

            for index, byte in enumerate(ip_address_bytes):
                self.sin_addr[index] = byte

        except Exception as e:
            raise Exception('Could not configure socket Instance', e)



if __name__ == "__main__":
    pass