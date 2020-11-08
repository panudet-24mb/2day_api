import os
from app.api.api import api
from app.models import *
from prometheus_sanic import monitor
import logging
from app.core import create_app
from dotenv import load_dotenv
import ssl


load_dotenv()

# logging.basicConfig(level=logging.DEBUG)
app = create_app()
app.blueprint(api)



if __name__ == "__main__":
    monitor(app , endpoint_type="url").expose_endpoint()
    context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("/home/ubuntu/cert.pem", keyfile="/home/ubuntu/key.pem")
    app.run(host="0.0.0.0" , port=4001 ,debug=True, workers=2 , ssl=context )
    # app.run(host="0.0.0.0" , port=4001 ,debug=True, workers=2  )