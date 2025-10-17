from flask import Flask, request, jsonify
from queue import Queue
import threading
import time

app = Flask(__name__)

# Cola compartida
task_queue = Queue()

# Simulación de procesamiento
def process_task(task):
    print(f"Procesando tarea: {task}")
    time.sleep(2)  # simula tarea pesada
    print(f"Tarea completada: {task}")

# Endpoint para agregar tareas a la cola
@app.route('/enqueue', methods=['POST'])
def enqueue():
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({"error": "Falta el campo 'task'"}), 400
    
    task = data['task']
    task_queue.put(task)
    return jsonify({"message": f"Tarea '{task}' agregada a la cola"}), 200

# Endpoint para procesar la siguiente tarea
@app.route('/process', methods=['GET'])
def process():
    if task_queue.empty():
        return jsonify({"message": "No hay tareas pendientes"}), 200

    task = task_queue.get()
    threading.Thread(target=process_task, args=(task,)).start()
    return jsonify({"message": f"Tarea '{task}' en proceso"}), 202

# Endpoint para ver el estado de la cola
@app.route('/status', methods=['GET'])
def status():
    return jsonify({"tareas_pendientes": task_queue.qsize()}), 200

if __name__ == '__main__':
    app.run(port=5000)