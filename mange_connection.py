# ::NOTE: (Most Important)*
# ------------------------------------------------------------------------------------------------------------------------------- #
# - This is the main file of this project that setup the server in a sense as it calls the server listner method to start ------- #
# ------------------- listening to the server and also handles all post and get requests made by the client --------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------- IMPORTING NECESSARY MODULES ------------------------------------------------- #
import time
from listen import StartListening
from server_errors import ConnectionTermination
from handle_requests import ListenHttpRequests, GiveRequestResponse


# ------------------------------------------------------------------------------------------------------------------------------- #
# ----------------------- SETTING UP THE CLASS RESPONSIBLE FOR LISTENING AND GIVING RESPONSE IN ORDER --------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #
class ConnectionManager(StartListening, GiveRequestResponse, ListenHttpRequests, ConnectionTermination):
    def __init__(self):
        StartListening.__init__(self)
        GiveRequestResponse.__init__(self)
        ListenHttpRequests.__init__(self)
        ConnectionTermination.__init__(self)
        

    def manage_server_connections(self) -> Exception:
        """
            -- This is the main method ; Call this method to start server and then interact with the client side file make_request
                to make get, post, put or delete requests. Request Processing is also managed here !

            -- NOTE: this method include send and recv system call utilization that are both IO-blocking Operations !
        """
        try:
            listening_socket : int = self.start_listner()

            while True:
                print(f"\n-> The server is listening at : IP = {self.host_ip_address}, Port = {self.available_port}")

                # ----------------------------------- Waiting for the host request and accepting ------------------------------- #
                client_socket, client_ip_address, client_port = self.confirm_connection(listening_socket)
                
                # --------------------------------- Reading the request from client and processing ----------------------------- #
                self.process_client_request(client_ip_address, client_socket, client_port)

        except KeyboardInterrupt:
            raise KeyboardInterrupt("The server stopped intentionally !")
        
        except Exception as e:
            raise Exception(f"Unable to listen on Server : {e}")
        
        finally:
            self.terminate_user_connection(self.libc_object, client_socket, client_ip_address, client_port, self.termination_message)
            self.libc_object.close(listening_socket)



    def confirm_connection(self, listening_socket) -> Exception | int:
        """
            -- Accepting the upcoming connection is the first step in a listening socket ; This is an IO-Blocking operation
                and after the connection socket creation server will wait for ay upcoming connection !

            -- NOTE: there is no need to use try catch here as methods that are being called have defined exception block and
                this method also gets called in an Exception block !
        """
        client_socket, client_ip_address, client_port, acceptance_message_length = self.accept_connection(listening_socket)
        self.display_server_side_logs(client_ip_address, client_port, acceptance_message_length)

        return client_socket, client_ip_address, client_port


    def process_client_request(self, client_ip_address, client_socket, client_port):
        """
            -- Procesing the request is what makes the Http Server Functional ; This is also an IO-Blocking Operation and
                once the connection is confirmed the server will connitue try to wait for client request and return them an
                appropriate response !

            -- NOTE: recv from libc is an IO-Blocking Operation but i'm not getting why calling that method here returns immediately ?
                to avoid operational error or empty recv method logic for only now accepting truthy outpus is implemented and
                a timeout of 10 seconds to terminate the connection to bound socket and release its resources !

            -- the logic for termination of connection from the client side is implemented here, As soon the connection is intrupted
                by the client server releases its resources.
        """
        start_time = time.time()
        while True:
            client_request, requested_url = self.understand_request(self.libc_object, client_socket)

            # -------------------------------- Terminating server connection if client refused ---------------------------------- #
            if not client_request and time.time() - start_time >= 10 or client_request == "RequestTermination":
                self.terminate_connection_enforced(client_socket, client_ip_address, client_port, client_request)
                break
            
            # ------------------------------------ Processing the request if its only valid ------------------------------------ #
            if client_request:
                print(f"\n-> Client : {client_ip_address} requested : {client_request} at route : {requested_url} using port : {client_port}")
                self.send_response(self.libc_object, client_socket, client_request, requested_url, client_ip_address)
                start_time = time.time()


    def terminate_connection_enforced(self, client_socket, client_ip_address, client_port, client_request):
        """
            -- termination of client connection in case of server issue or client refuse !
        """
        try:
            self.libc_object.close(client_socket)
            if client_request == "RequestTermination":
                print(f"\n-> Connection Terminated by client : {client_ip_address} at port : {client_port}")
            
            else:
                print(f"\n-> Connection Timeout for client : {client_ip_address} at port : {client_port}")
        
        except Exception as e:
            raise Exception(f"Unable to close client socket for resource allocation ; {e}")



if __name__ == '__main__':
    system = ConnectionManager()
    system.manage_server_connections()
