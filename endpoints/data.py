import os
import sys
sys.path.insert(0, os.getcwd())

class EndpointData:
    name = None
    endpoint = "/"
    args = []
    api_prefix = '/api/v1'
    origins = [
        "localhost", 
        "http://localhost:3000",
        "http://localhost:9002",
    ]

    def __init__(self, name: str, endpoint: str, args: list):
        self.name = name
        self.endpoint = endpoint
        self.args = args

context_data = EndpointData("Context", "/context", [])