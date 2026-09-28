from flask import Flask
import redis

app = Flask(__name__)

# conectar a redis (nombre del servicio = hostname)
r = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route("/")
def home():
    contador = r.get("contador")
    if contador is None:
        contador = 0
    return f"Contador actual: {contador}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)