from flask import Flask, request, json
app = Flask(__name__)
@app.route('/post_json', methods=['POST'])
def process_json():
    data = json.loads(request.data)
    print(f'data={data}')
    result = 'ResultOk'
    return result

if __name__ == "__main__":
    app.run()