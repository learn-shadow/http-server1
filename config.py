# ::NOTE: (Most Important)*
# ------------------------------------------------------------------------------------------------------------------------------- #
# - Configuration files are backone of any project ; I just preffered to use json format configuration file for this project as - #
# - i'm not hoping to this file go over even 20 lines. All of the parameters that are used are extracted in seperate instance --- #
# --------- variables ; This file loads the whole configuration file at once and then poppulate the instance variables ---------- #
# ------------------------------------------------------------------------------------------------------------------------------- #


# ------------------------------------------------- IMPORTING NECESSARY MODULES ------------------------------------------------- #
import json


# ------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------- SETTING UP THE CLASS RESPONSIBLE FOR FETCHING AND PROVIDING CONFIGURATION ------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------- #
class ConfigurationFetcher:
    def __init__(self):
        """
            -- NOTE: You must not change this constructor untill you haven't addedd any line to the configuration file or have
                changed any file ! It can cause persistent issue accross the project files !
        """
        # --------------------------------------------- Configuration file data ------------------------------------------------- #
        self.configuration_file_name : str = "config.json"

        self.connection_type : str = "connection_type"
        self.connection_type1 : str = "ipv4_connection"
        self.connection_type2 : str = "ipv6_connection"
        
        self.protocol_type : str = "protocol_type"
        self.protocol_type1 : str = "tcp_protocol"
        self.protocol_type2 : str = "udp_protocol"

        self.stream_type : str = "stream_type"
        self.stream_type1 : str = "sock_stream"
        self.stream_type2 : str = "sock_drgam"

        self.machine_data : str = "machine_data"
        self.host_info : str = "host_address"
        self.port_info : str = "available_port"

        # ---------------------------------------------- Loading data in memory ----------------------------------------------- #
        self.configuration_data : dict[str : str] = self.load_configuration()

        # ------------------------------------------- Populating instance variables ------------------------------------------- #
        self.ipv4_connection : int = self.configuration_data[self.connection_type][self.connection_type1]
        self.ipv6_connection : int = self.configuration_data[self.connection_type][self.connection_type2]

        self.tcp_protocol : int = self.configuration_data[self.protocol_type][self.protocol_type1]
        self.udp_protocol : int = self.configuration_data[self.protocol_type][self.protocol_type2]

        self.sock_stream : int = self.configuration_data[self.stream_type][self.stream_type1]
        self.sock_dgram : int = self.configuration_data[self.stream_type][self.stream_type2]
        

        self.host_address : list[int] | tuple[int] = self.configuration_data[self.machine_data][self.host_info]
        self.available_port : list[int] | tuple[int] = self.configuration_data[self.machine_data][self.port_info]



    def load_configuration(self) -> int | list[int] | tuple[int] | Exception:
        """
            -- NOTE: The configuration file needs to be located in the same directory where the config file is located.
        """
        try:
            with open(self.configuration_file_name) as file:
                file_data = json.load(file)
                return file_data

        except FileNotFoundError:
            raise FileNotFoundError(f"Unable to find configuration file in the same directory...")
        
        except UnicodeDecodeError:
            raise UnicodeDecodeError(f"Unable to decode configuration file, please ensure it's in correct JSON format...")
        
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f"Unable to parse configuration file, please ensure it's in correct JSON format...")
        
        except ConnectionError:
            raise ConnectionError("Unable to connect to configuration file")
        
        except Exception as e:
            raise Exception(f"Unable to parse configuration file : {e}")
        




if __name__ == "__main__":
    pass