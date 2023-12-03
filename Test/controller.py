import time
from typing import Dict, Any
from flask import Flask, jsonify, request, render_template, Response

app = Flask(__name__)

# Initial tasks data
tasks = [
    {
        'id': 1,
        'title': 'Shopping',
        'description': 'Buy groceries from the store',
        'creation_date': '2023-11-08',
        'attachments': [],
        'categories': []
    },
    {
        'id': 2,
        'title': 'Cleaning',
        'description': 'Clean the apartment',
        'creation_date': '2023-11-20',
        'attachments': [],
        'categories': ['Home tasks']
    }
]


# Homepage route
@app.route('/')
def index():
    return render_template('site.html')


# Get filtered tasks route
@app.route('/tasks', methods=['GET'])
def get_filtered_tasks():
    # Retrieve sort_type and filter_priority from query parameters
    sort_type = request.args.get('sort', 'asc')  # Default to ascending order
    filter_priority = request.args.get('priority', '')

    # Filter tasks based on priority
    filtered_tasks = tasks
    if filter_priority:
        filtered_tasks = [task for task in tasks if task.get('priority') == filter_priority]

    # Sort tasks based on creation_date
    sorted_tasks = sorted(filtered_tasks, key=lambda x: x['creation_date'], reverse=(sort_type == 'desc'))

    return jsonify({'tasks': sorted_tasks})


# Create task route
@app.route('/tasks', methods=['POST'])
def create_task() -> Response:
    # Get JSON data from the request
    data: Dict[str, Any] = request.get_json()

    # Get the current date
    current_date: str = time.strftime('%Y-%m-%d')

    # Create a new task
    new_task: Dict[str, Any] = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'description': data['description'],
        'creation_date': current_date,
        'attachments': data.get('attachments', []),
        'categories': data.get('categories', []),
        'priority': data.get('priority', []),
    }

    # Add the new task to the tasks list
    tasks.append(new_task)

    # Create a response with the new task data
    response: Response = jsonify({'task': new_task})
    response.status_code = 201  # Set HTTP status code to 201 (Created)
    return response


# Get all tasks route
@app.route('/tasks', methods=['GET'])
def get_all_tasks():
    # Return all tasks as JSON
    return jsonify({'tasks': tasks})


# Get task by ID route
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    # Find the task with the given ID
    task = next((task for task in tasks if task['id'] == task_id), None)

    # If task is not found, return a 404 error
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    # Return the task data as JSON
    return jsonify({'task': task})


# Update task route
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    # Find the task with the given ID
    task = next((task for task in tasks if task['id'] == task_id), None)

    # If task is not found, return a 404 error
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    # Get JSON data from the request
    data = request.get_json()

    # Update task properties if provided in the request data
    task['title'] = data.get('title', task['title'])
    task['description'] = data.get('description', task['description'])
    task['attachments'] = data.get('attachments', task['attachments'])
    task['categories'] = data.get('categories', task['categories'])

    # Update priority only if 'priority' is present in the request data
    if 'priority' in data:
        task['priority'] = data['priority']

    # Return the updated task data as JSON
    return jsonify({'task': task})


# Delete task route
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Remove the task with the given ID from the tasks list
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]

    # Return a success message as JSON
    return jsonify({'result': True})


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
