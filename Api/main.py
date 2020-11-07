import os
from app.core import create_app
import json

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0" , port=8080 ,debug=True,workers=2  )
