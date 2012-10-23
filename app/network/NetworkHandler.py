# This will provide an interface to the network for the main app

''' Functions to start a server/client pair or a single client will be provided
        This function will handle the creation of those objects
            And the launching/killing of their network threads
    The main app will then be able to send network data without caring if it is
    a server or a client

    This class will also notify the main app upon network termination
        And allow for remote termination from the network app
'''
