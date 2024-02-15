document.addEventListener('DOMContentLoaded', () => {
    const taskListElement = document.getElementById('taskList');
    const addTaskForm = document.getElementById('addTaskForm');
    const editTaskForm = document.getElementById('editTaskForm');
    const editTitleInput = document.getElementById('editTitle');
    const editDescriptionInput = document.getElementById('editDescription');
    const editCategoriesInput = document.getElementById('editCategories');
    const editFileAttachmentInput = document.getElementById('editFileAttachment');
    const editPriorityInput = document.getElementById('editPriority');
    const updateTaskButton = document.getElementById('updateTaskButton');
    const searchTaskButton = document.getElementById('searchTaskButton');
    const sortTypeSelect = document.getElementById('sortType');
    const filterPrioritySelect = document.getElementById('filterPriority');

    // Функция удаления дубликатов
    function removeDuplicates(tasks) {
        const uniqueTasks = [];
        const taskIds = new Set();

        tasks.forEach(task => {
            if (!taskIds.has(task.id)) {
                taskIds.add(task.id);
                uniqueTasks.push(task);
            }
        });

        return uniqueTasks;
    }

    function handleInitializationError(error) {
        console.error('Error during initialization:', error);
    }

    async function fetchTasks() {
        try {
            const response = await fetch('/api/tasks?sort=asc');
            if (!response.ok) {
                console.error('Error fetching tasks');
                return Promise.reject('Error fetching tasks');
            }

            const tasks = await response.json();
            const uniqueTasks = removeDuplicates(tasks);

            uniqueTasks.forEach(task => {
                createTaskElement(task);
            });
        } catch (error) {
            console.error('Error fetching tasks:', error);
            return Promise.reject(error);
        }
    }

    async function addTask(event) {
        event.preventDefault();
        const titleInput = document.getElementById('title');
        const descriptionInput = document.getElementById('description');
        const categoriesInput = document.getElementById('categories');
        const fileAttachmentInput = document.getElementById('fileAttachment');
        const priorityInput = document.getElementById('priority');

        const newTask = {
            title: titleInput.value,
            description: descriptionInput.value,
            categories: categoriesInput.value,
            fileAttachment: fileAttachmentInput.value,
            priority: priorityInput.value
        };

        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(newTask)
            });

            if (!response.ok) {
                console.error('Error adding task');
                return;
            }

            const data = await response.json();
            createTaskElement(data);

            // Сохраняем задачи в localStorage
            const tasks = JSON.parse(localStorage.getItem('tasks')) || [];
            tasks.push(data);
            localStorage.setItem('tasks', JSON.stringify(tasks));

            // Используем новый метод для фильтрации задач по приоритету
            await filterTasksByPriority(filterPrioritySelect.value);
        } catch (error) {
            console.error('Error adding task:', error);
        }

        titleInput.value = '';
        descriptionInput.value = '';
        categoriesInput.value = '';
        fileAttachmentInput.value = '';
        priorityInput.value = 'low';
    }

    async function downloadFile(taskId) {
        try {
            const response = await fetch(`/api/tasks/${taskId}/download`);

            if (!response.ok) {
                console.error('Ошибка при скачивании файла');
                return;
            }

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);

            const a = document.createElement('a');
            a.href = url;
            a.download = `task_${taskId}_file`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        } catch (error) {
            console.error('Ошибка при скачивании файла:', error);
        }
    }
    async function uploadFile(taskId) {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.click();

        fileInput.addEventListener('change', async function () {
            downloadFile(taskId);
        });
    }

    function createTaskElement(task) {
        const listItem = document.createElement('li');
        listItem.id = `task-${task.id}`;

        const taskInfo = document.createElement('span');
        taskInfo.textContent =
            `ID: ${task.id}, Заголовок: ${task.title}, Описание: ${task.description}, Категории: ${task.categories}, Вложенный файл: ${task.fileAttachment}, Приоритет: ${task.priority}, Дата: ${new Date(task.date).toLocaleString()}`;

        listItem.appendChild(taskInfo);

        const editButton = document.createElement('button');
        editButton.textContent = 'Редактировать';
        editButton.className = 'editButton';
        editButton.style.marginLeft = '10px';
        editButton.dataset.taskId = task.id;
        editButton.addEventListener('click', () => {
            editTask(task);
        });

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Удалить';
        deleteButton.addEventListener('click', async () => {
            await deleteTask(task.id);
        });

        const uploadButton = document.createElement('button');
        uploadButton.textContent = 'Загрузить файл';
        uploadButton.style.right = '120px';
        uploadButton.addEventListener('click', () => {
            uploadFile(task.id);
        });

        listItem.appendChild(uploadButton);

        const downloadButton = document.createElement('button');
        downloadButton.textContent = 'Скачать файл';
        downloadButton.style.marginLeft = '10px';
        downloadButton.addEventListener('click', () => {
            downloadFile(task.id, task.fileAttachment);
        });

        listItem.appendChild(downloadButton);

        switch (task.priority) {
            case 'high':
                listItem.style.backgroundColor = 'red';
                break;
            case 'medium':
                listItem.style.backgroundColor = '#f4bafe';
                break;
            case 'low':
                listItem.style.backgroundColor = 'aqua';
                break;
            default:
                listItem.style.backgroundColor = 'lightgray';
                break;
        }

        listItem.appendChild(editButton);
        listItem.appendChild(deleteButton);
        taskListElement.appendChild(listItem);
    }

    function editTask(task) {
        editTitleInput.value = task.title;
        editDescriptionInput.value = task.description;
        editCategoriesInput.value = task.categories;
        editFileAttachmentInput.value = task.fileAttachment;
        editPriorityInput.value = task.priority;

        editTaskForm.style.display = 'block';

        updateTaskButton.dataset.taskId = task.id;

        updateTaskButton.onclick = async () => {
            const taskIdToUpdate = updateTaskButton.dataset.taskId;

            try {
                await updateTask(taskIdToUpdate);
            } catch (error) {
                console.error('Error updating task:', error);
            }
        };
    }

    async function updateTask(taskId) {
        const updatedTask = {
            title: editTitleInput.value,
            description: editDescriptionInput.value,
            categories: editCategoriesInput.value,
            fileAttachment: editFileAttachmentInput.value,
            priority: editPriorityInput.value
        };

        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(updatedTask)
            });

            if (!response.ok) {
                console.error('Error updating task');
                return;
            }

            const data = await response.json();
            const updatedTaskElement = document.getElementById(`task-${taskId}`);

            if (updatedTaskElement) {
                updatedTaskElement.querySelector('span').textContent =
                    `ID: ${taskId}, Title: ${data.title}, Description: ${data.description}, Categories: ${data.categories}, File Attachment: ${data.fileAttachment}, Priority: ${data.priority}, Date: ${new Date(data.date).toLocaleString()}`;

                switch (data.priority) {
                    case 'high':
                        updatedTaskElement.style.backgroundColor = 'red';
                        break;
                    case 'medium':
                        updatedTaskElement.style.backgroundColor = '#f4bafe';
                        break;
                    case 'low':
                        updatedTaskElement.style.backgroundColor = 'aqua';
                        break;
                    default:
                        updatedTaskElement.style.backgroundColor = 'lightgray';
                        break;
                }
            }

            editTaskForm.style.display = 'none';

        } catch (error) {
            console.error('Error updating task:', error);
        }
    }

    async function deleteTask(taskId) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'DELETE'
            });

            if (response.status === 204) {
                const deletedTaskElement = document.getElementById(`task-${taskId}`);
                if (deletedTaskElement) {
                    deletedTaskElement.remove();
                }
                await filterTasksByPriority(filterPrioritySelect.value);
            } else if (response.status === 404) {
                console.error('Task not found');
            } else {
                console.error('Error:', response.status);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }



    function searchTask() {
        const taskIdInput = document.getElementById('taskId');
        const taskIdToSearch = parseInt(taskIdInput.value);

        if (!isNaN(taskIdToSearch) && taskIdToSearch >= 1) {
            fetch(`/api/tasks/${taskIdToSearch}`)
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else if (response.status === 404) {
                        return null;
                    } else {
                        throw new Error('Error fetching task');
                    }
                })
                .then(foundTask => {
                    const searchResult = document.getElementById('searchResult');
                    if (foundTask) {
                        searchResult.innerText = `ID: ${foundTask.id}, Title: ${foundTask.title}, Description: ${foundTask.description}, Categories: ${foundTask.categories}, File Attachment: ${foundTask.fileAttachment}, Priority: ${foundTask.priority}, Date: ${new Date(foundTask.date).toLocaleString()}`;
                    } else {
                        searchResult.innerText = 'Task not found.';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        } else {
            document.getElementById('searchResult').innerText = 'Please enter a valid task number.';
        }
    }

    async function sortTasksByDate(sortType) {
        try {
            const response = await fetch(`/api/tasks?sort=${sortType}`);
            if (!response.ok) {
                console.error('Error fetching tasks');
                return;
            }

            const tasks = await response.json();
            const uniqueTasks = removeDuplicates(tasks);

            taskListElement.innerHTML = '';

            uniqueTasks.forEach(task => {
                createTaskElement(task);
            });

            // Фильтрация по приоритету после сортировки по дате
            await filterTasksByPriority(filterPrioritySelect.value);
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function filterTasksByPriority(priority) {
        let url = '/api/tasks';
        if (priority) {
            url += `/priority/${priority}`;
        }

        try {
            const response = await fetch(url);
            if (!response.ok) {
                console.error('Error fetching tasks');
                return;
            }

            const tasks = await response.json();
            taskListElement.innerHTML = '';

            const uniqueTasks = removeDuplicates(tasks);
            uniqueTasks.forEach(task => {
                createTaskElement(task);
            });
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function setupEventListeners() {
        searchTaskButton.addEventListener('click', searchTask);
        addTaskForm.addEventListener('submit', addTask);

        sortTypeSelect.addEventListener('change', async () => {
            await sortTasksByDate(sortTypeSelect.value);
        });

        filterPrioritySelect.addEventListener('change', async () => {
            await filterTasksByPriority(filterPrioritySelect.value);
        });
    }
    fetchTasks().then(setupEventListeners).catch(handleInitializationError);
});
