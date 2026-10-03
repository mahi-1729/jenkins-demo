#def add(a, b):
#    return a + b


#def get_message():
#    return "Hello from Jenkins CI!"


#if __name__ == "__main__":
#    print(get_message())
#    print("2 + 3 =", add(2, 3))

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello from Jenkins CI/CD running inside Docker!"


@app.route("/health")
def health():
    return {
        "status": "DOWN"
    }, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
