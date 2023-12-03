document.addEventListener('DOMContentLoaded', function () {
    const taskListElement = document.getElementById('taskList');
    const addTaskForm = document.getElementById('addTaskForm');
    const searchTaskButton = document.getElementById('searchTaskButton');
    const searchResultElement = document.getElementById('searchResult');
    const sortTypeSelect = document.getElementById('sortType');
    const applySortButton = document.getElementById('applySortButton');
    const filterPrioritySelect = document.getElementById('filterPriority');

    // Function to update the task list based on sorting and filtering
    function updateTaskList() {
        const sortType = sortTypeSelect.value;
        const filterPriority = filterPrioritySelect.value;

        fetch(`/tasks?sort=${sortType}&priority=${filterPriority}`)
            .then(response => response.json())
            .then(data => {
                taskListElement.innerHTML = '';

                if (data && data.tasks && Array.isArray(data.tasks)) {
                    data.tasks.forEach(task => {
                        const listItem = document.createElement('li');
                        const taskInfo = document.createElement('span');

                        // Display task information
                        taskInfo.textContent = `ID: ${task.id}, Title: ${task.title}, Description: ${task.description}, Created: ${task.creation_date}, Category: ${task.categories.join(', ')}, Attachments: ${task.attachments.length}`;

                        // Create Edit button
                        const editButton = document.createElement('button');
                        editButton.textContent = 'Edit';
                        editButton.style.marginRight = '75px';
                        editButton.addEventListener('click', () => editTask(task.id));

                        // Create Delete button
                        const deleteButton = document.createElement('button');
                        deleteButton.textContent = 'Delete';
                        deleteButton.addEventListener('click', () => deleteTask(task.id));

                        // Create Download Attachment button
                        const downloadButton = document.createElement('button');
                        downloadButton.textContent = 'Download Attachment';
                        downloadButton.style.marginRight = '135px';
                        downloadButton.addEventListener('click', () => downloadAttachment(task.id));

                        // Apply background color based on priority
                        if (task.priority === 'high') {
                            listItem.style.backgroundColor = 'red';
                        } else if (task.priority === 'medium') {
                            listItem.style.backgroundColor = 'yellow';
                        } else if (task.priority === 'low') {
                            listItem.style.backgroundColor = 'green';
                        }

                        listItem.appendChild(taskInfo);
                        listItem.appendChild(editButton);
                        listItem.appendChild(deleteButton);
                        listItem.appendChild(downloadButton);

                        taskListElement.appendChild(listItem);
                    });
                } else {
                    console.error('Error updating task list: Invalid server response format');
                }
            })
            .catch(error => console.error('Error updating task list:', error));
    }

    // Function to add a new task
    function addTask() {
        // Fetch values from the form
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const categories = document.getElementById('categories').value;
        const priority = document.getElementById('priority').value;

        // Make a POST request to add a new task
        fetch('/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description,
                categories: categories.split(',').map(category => category.trim()),
                creation_date: new Date().toISOString(),
                priority: priority,
            }),
        })
            .then(response => response.json())
            .then(data => {
                updateTaskList();
            })
            .catch(error => console.error('Error adding task:', error));
    }

    // Function to delete a task
    function deleteTask(taskId) {
        // Make a DELETE request to delete the specified task
        fetch(`/tasks/${taskId}`, {
            method: 'DELETE',
        })
            .then(response => response.json())
            .then(data => {
                updateTaskList();
            })
            .catch(error => console.error('Error deleting task:', error));
    }

    // Function to retrieve task data for editing
    function editTask(taskId) {
        // Make a GET request to retrieve task data for editing
        fetch(`/tasks/${taskId}`)
            .then(response => response.json())
            .then(data => {
                const editForm = document.getElementById('editTaskForm');
                const updateButton = document.getElementById('updateTaskButton');

                // Populate edit form fields with task data
                document.getElementById('editTitle').value = data.task.title;
                document.getElementById('editDescription').value = data.task.description;
                document.getElementById('editCategories').value = data.task.categories.join(', ');
                document.getElementById('editPriority').value = data.task.priority;

                // Show the edit form
                editForm.style.display = 'block';

                // Clear any previous click event listener on the update button
                updateButton.onclick = null;

                // Set up a new event listener for updating the task
                updateButton.onclick = () => updateTask(taskId);
            })
            .catch(error => console.error('Error getting data for editing task:', error));
    }

    // Function to update an existing task
    function updateTask(taskId) {
        // Fetch updated values from the edit form
        const title = document.getElementById('editTitle').value;
        const description = document.getElementById('editDescription').value;
        const categories = document.getElementById('editCategories').value;
        const priority = document.getElementById('editPriority').value;

        // Make a PUT request to update the specified task
        fetch(`/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description,
                categories: categories.split(',').map(category => category.trim()),
                priority: priority,
            }),
        })
            .then(response => response.json())
            .then(data => {
                // Hide the edit form after updating
                document.getElementById('editTaskForm').style.display = 'none';
                // Update the task list
                updateTaskList();
            })
            .catch(error => console.error('Error updating task:', error));
    }

    // Function to download an attachment for a task
    function downloadAttachment(taskId) {
        // Make a GET request to download the attachment for the specified task
        fetch(`/tasks/${taskId}/download`, {
            method: 'GET',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.blob();
            })
            .then(blob => {
                // Create a link and trigger a click event to download the attachment
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = `attachment_task_${taskId}`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            })
            .catch(error => console.error('Error downloading attachment:', error));
    }

    // Function to search for a task by ID
    function searchTask(taskId) {
        // Make a GET request to search for a task by ID
        fetch(`/tasks/${taskId}`)
            .then(response => response.json())
            .then(data => {
                const resultMessage = data.error ? data.error : `Task Found: ID: ${data.task.id}, Title: ${data.task.title}, Description: ${data.task.description}, Created: ${data.task.creation_date}`;
                searchResultElement.textContent = resultMessage;
            })
            .catch(error => console.error('Error searching for task:', error));
    }

    // Event handler for the form to add a task
    addTaskForm.addEventListener('submit', function (event) {
        event.preventDefault();
        addTask();
    });

    // Event handler for the button to search for a task
    searchTaskButton.addEventListener('click', function () {
        const taskId = document.getElementById('taskId').value;
        searchTask(taskId);
    });

    // Event handler for the button to apply sorting
    applySortButton.addEventListener('click', function () {
        updateTaskList();
    });

    // Event handler for selecting a sorting type
    sortTypeSelect.addEventListener('change', function () {
        updateTaskList();
    });

    // Event handler for selecting a priority filter
    filterPrioritySelect.addEventListener('change', function () {
        updateTaskList();
    });

    // Initial update of the task list on page load
    updateTaskList();

    // Event handler for the button to apply sorting (additional handling)
    applySortButton.addEventListener('click', function () {
        updateTaskList();
    });
});
