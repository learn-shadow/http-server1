# ::NOTE: (Most Important)*
# ------------------------------------------------------------------------------------------------------------------------------- #
# - This file include the code that is used to listen the upcoming http request from the client. It has two seperate classess --- #
# - one where the logic for understanding the request is implemented and the other is used to send back the appropriate --------- #
# ----------------------------- response after analysing the requested url and request method ! --------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------- IMPORTING NECESSARY MODULES ------------------------------------------------- #
import os
import ctypes
from get_request import DefinedGetRoutes
from put_request import DefinedPutRoutes
from post_request import DefinedPostRoutes
from delete_request import DefinedDeleteRoutes
from server_errors import UndefinedRequestMethod



# ------------------------------------------------------------------------------------------------------------------------------- #
# -------------------- SETTING UP THE CLASS RESPONSIBLE FOR UNDERSTANDING THE GIVEN REQUEST FROM CLIENT ------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #
class ListenHttpRequests:
    def catch_upcoming_request(self, libc_object, client_socket) -> Exception | str:
        """
            -- Using recv system call we indefinately listen for incoming requests from clients and just decoding that request
                for processing !
        """
        try:
            message_buffer = ctypes.create_string_buffer(1024)
            request = libc_object.recv(client_socket, message_buffer, 1024, 0)

            if request < 0:
                raise Exception(f"Unable to receive request from client : {os.strerror(ctypes.get_errno())}")
            
            return message_buffer.value.decode("utf-8")
        
        except ConnectionError:
            raise ConnectionError("Unable to Connect to the client...!")
        
        except Exception as e:
            raise Exception(f"Unable to catch up with client request : {e}")


    def understand_request(self, libc_object, client_socket) -> str | Exception | bool:
        """
            -- NOTE: Parsinng the incoming cleint request and extracting the information like method type and requested url
                for now only !
        """
        try:
            client_request : str = self.catch_upcoming_request(libc_object, client_socket)
            split_client_request = client_request.split()
            client_request_length : int = len(split_client_request)

            if client_request_length == 1:
                return "RequestTermination", "RequestTermination"

            elif client_request_length >= 2:
                request_method = split_client_request[0]
                requested_url = split_client_request[1]

                return request_method, requested_url
            
            return False, False

        except Exception as e:
            raise Exception(f"Unable to understand client request : {e}")




# ------------------------------------------------------------------------------------------------------------------------------- #
# ------------------------ SETTING UP THE CLASS RESPONSIBLE FOR SENDING BACK A RESPONSE TO THE CLIENT --------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #
class GiveRequestResponse(ListenHttpRequests):
    """
        -- Workflow for this class goes like this !
            1 - Each request type has its own dedicated defined class.
            2 - we analyse the request type and then call the resultant class for response !
    """
    def  __init__(self):
        """
            -- Defining allowed methods and using composition to avoid Diamond Inheritance problem by any mean
        """
        self.get_request : str = "GET"
        self.post_request : str = "POST"
        self.put_request : str = "PUT"
        self.delete_request : str = "DELETE"
        self.get_response : DefinedGetRoutes = DefinedGetRoutes()
        self.post_response : DefinedPostRoutes = DefinedPostRoutes()
        self.put_response : DefinedPutRoutes = DefinedPutRoutes()
        self.delete_response : DefinedDeleteRoutes = DefinedDeleteRoutes()
        self.undefined_method : UndefinedRequestMethod = UndefinedRequestMethod()


    def send_response(self, libc_object, client_socket, request_type, requested_url, client_ip_address) -> Exception:
        """
            -- Analysing the request type and calling the appropriate class method !
        """
        if request_type ==  self.get_request:
            self.get_response.give_get_response(libc_object, client_socket, requested_url, client_ip_address)

        elif request_type == self.post_request:
            self.post_response.give_post_response(libc_object, client_socket, requested_url, client_ip_address)

        elif request_type == self.put_request:
            self.put_response.give_put_response(libc_object, client_socket, requested_url, client_ip_address)

        elif request_type == self.delete_request:
            self.delete_response.give_delete_response(libc_object, client_socket, requested_url, client_ip_address)

        else:
            self.undefined_method.return_undefined_method_call(libc_object, client_socket)




if __name__ == '__main__':
    pass