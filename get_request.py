# ::NOTE: (Most Important)*
# ------------------------------------------------------------------------------------------------------------------------------- #
# - This file contains the definition of all get requests which server can response, If you want to add some new methods kindly - #
# - add them for yourself following the same schema or just write one, Well this script do not share any html content or -------  #
# ----------- anything else like that ; For the sake of simplicity only the bytes of some data types gets shared ---------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #




# ------------------------------------------------- IMPORTING NECESSARY MODULES ------------------------------------------------- #
import os
import random
from server_errors import AddressNotFoundException


# ------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------- CLASS THAT IS RESPONSIBLE FOR GET REQUETS DEFINITION --------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------------- #
class DefinedGetRoutes(AddressNotFoundException):
    def __init__(self):
        """
            -- To add a new method request route for simulation just create an instance level variable and assign the path to it.
                NOTE: Don't forget to do change the make requests file if you change here. Follow that file instructions. Also
                    Make sure you add your variable to available list as well ; The system first checks if the path is present
                    in the list or not ?
        """
        super().__init__()
        self.home_route : str = "/"
        self.about_route : str = "/about"
        self.contact_route : str = "/contact"
        self.generate_randoms : str = "/generate_randoms"
        self.return_server_directory : str = "/my-folder-view"
        self.available_list : list[str] = [self.home_route, self.about_route, self.contact_route, self.generate_randoms,
            self.return_server_directory
        ]


    def give_get_response(self, libc_object, client_socket, requested_url, client_ip_address) -> Exception | bytes:
        """
            -- main method that gets called in the handle_request.py and it calls the appropriate method if present !
        """
        if requested_url in self.available_list:
            if requested_url == self.home_route:
                message = self.send_home_page(libc_object, client_socket, client_ip_address)
                print(f":: Resource {message} shared to client : {client_ip_address} in response of {requested_url}")

            elif requested_url == self.about_route:
                message = self.send_about_page(libc_object, client_socket, client_ip_address)
                print(f":: Resource {message} shared to client : {client_ip_address} in response of {requested_url}")

            elif requested_url == self.contact_route:
                message = self.send_contact_page(libc_object, client_socket, client_ip_address)
                print(f":: Resource {message} shared to client : {client_ip_address} in response of {requested_url}")

            elif requested_url == self.generate_randoms:
                message = self.send_random_page(libc_object, client_socket, client_ip_address)
                print(f":: Resource {message} shared to client : {client_ip_address} in response of {requested_url}")

            elif requested_url == self.return_server_directory:
                message = self.send_user_directory(libc_object, client_socket, client_ip_address)
                print(f":: System Directory data to client : {client_ip_address} gets shared in response of {requested_url}")

        else:
            message = self.return_404_error(libc_object, client_socket, client_ip_address)
            print(f":: Resource {message} shared to client : {client_ip_address} in response of {requested_url}")


    @staticmethod
    def send_user_directory(libc_object, client_socket, client_ip_address) -> Exception | str:
        try:
            client_directory = os.listdir(os.getcwd())
            client_directory = b', '.join(bytes(str(file), 'utf8') for file in client_directory)
            result = libc_object.send(client_socket, client_directory, len(client_directory), 0)

            if result < 0:
                raise Exception(f"Unable to send directory data to client : {client_ip_address}")

            return client_directory
        
        except ConnectionError:
            raise ConnectionError(f"Unable to send directory data to client : {client_ip_address}")
        
        except Exception as e:
            raise Exception(f"Unable to send diretory data to client : {client_ip_address} Cause : {e}")
    

    @staticmethod
    def send_home_page(libc_object, client_socket, client_ip_address) -> Exception | str:
        try:
            home_message = b"Home Page has been delivered to you Successfully !"
            result = libc_object.send(client_socket, home_message, len(home_message), 0)

            if result < 0:
                raise Exception(f"Unable to send home message to client : {client_ip_address}")

            return home_message
        
        except ConnectionError:
            raise ConnectionError(f"Unable to send home message to client : {client_ip_address}")
        
        except Exception as e:
            raise Exception(f"Unable to send home message to client : {client_ip_address} Cause : {e}")
    

    @staticmethod
    def send_about_page(libc_object, client_socket, client_ip_address) -> Exception | str:
        try:
            about_message = b"About Page has been delivered to you Successfully !"
            result = libc_object.send(client_socket, about_message, len(about_message), 0)

            if result < 0:
                raise Exception(f"Unable to send about message to client : {client_ip_address}")
            
            return about_message
        
        except ConnectionError:
            raise ConnectionError(f"Unable to send about message to client : {client_ip_address}")
        
        except Exception as e:
            raise Exception(f"Unable to send about message to client : {client_ip_address} Cause : {e}")


    @staticmethod
    def send_contact_page(libc_object, client_socket, client_ip_address) -> Exception | str:
        try:
            contact_message = b"Contact Page has been delivered to you Successfully !"
            result = libc_object.send(client_socket, contact_message, len(contact_message), 0)

            if result < 0:
                raise Exception(f"Unable to send contact message to client : {client_ip_address}")
            
            return contact_message
        
        except ConnectionError:
            raise ConnectionError(f"Unable to send contact message to client : {client_ip_address}")
        
        except Exception as e:
            raise Exception(f"Unable to send contact message to client : {client_ip_address} Cause : {e}")
        

    @staticmethod
    def send_random_page(libc_object, client_socket, client_ip_address) -> Exception | str :
        try:
            random_message = [random.randint(1, 10) for _ in range(10)]
            random_message = b''.join(bytes(str(number), 'utf8') for number in random_message)
            result = libc_object.send(client_socket, random_message, len(random_message), 0)

            if result < 0:
                raise Exception(f"Unable to send random message to client : {client_ip_address}")
            return random_message
        
        except ConnectionError:
            raise ConnectionError(f"Unable to send random message to client : {client_ip_address}")
        
        except Exception as e:
            raise Exception(f"Unable to send random message to client : {client_ip_address} Cause : {e}")



if __name__ == '__main__':
    pass