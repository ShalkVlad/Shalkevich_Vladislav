package com.Test.demo.services;

import com.Test.demo.models.Task;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class TaskService {

    // Logger for logging messages
    public static final Logger logger = LoggerFactory.getLogger(TaskService.class);

    // List to store tasks
    private final List<Task> tasks = new ArrayList<>();

    // Variable to keep track of the last assigned ID
    private int lastAssignedId = 0;

    // Get all tasks
    public List<Task> getAllTasks() {
        return tasks;
    }

    // Add a task to the list with an automatically generated ID
    public void addTask(Task task) {
        // Increment the last assigned ID before assigning it to the new task
        lastAssignedId++;
        task.setId(lastAssignedId);
        tasks.add(task);
    }

    // Delete an image from a task
    public void deleteImageFromTask(int taskId, String imagePath) {
        Task task = getTaskById(taskId);
        if (task != null) {
            if (!task.getPdfAttachments().remove(imagePath)) {
                logger.warn("Image path '{}' not found in task with ID '{}'", imagePath, taskId);
            }
        } else {
            logger.warn("Task with ID '{}' not found while deleting image '{}'", taskId, imagePath);
        }
    }


    // Update an image in a task
    public void updateImageInTask(int taskId, String oldImagePath, String newImagePath) {
        Task task = getTaskById(taskId);
        if (task != null) {
            List<String> pdfAttachments = task.getPdfAttachments();
            int index = pdfAttachments.indexOf(oldImagePath);
            if (index != -1) {
                pdfAttachments.set(index, newImagePath);
            }
        }
    }

    // Get tasks by category
    public List<Task> getTasksByCategory(String category) {
        return tasks.stream()
                .filter(task -> task.getCategories().contains(category))
                .collect(Collectors.toList());
    }

    // Link images to a task
    public void linkImagesToTask(int taskId, List<String> imagePaths) {
        Task task = getTaskById(taskId);
        if (task != null) {
            task.setPdfAttachments(imagePaths);
        }
    }

    // Get all tasks sorted by title
    public List<Task> getAllTasksSortedByTitle(String sortOrder) {
        Comparator<Task> comparator = Comparator.comparing(Task::getTitle);
        if ("desc".equalsIgnoreCase(sortOrder)) {
            comparator = comparator.reversed();
        }
        return tasks.stream()
                .sorted(comparator)
                .collect(Collectors.toList());
    }

    // Add an attachment to a task
    public void addAttachmentToTask(int taskId, String attachment) {
        Task task = getTaskById(taskId);
        if (task != null) {
            task.getPdfAttachments().add(attachment);
        }
    }

    // Get a task by its ID
    public Task getTaskById(int taskId) {
        for (Task task : tasks) {
            if (task.getId() == taskId) {
                return task;
            }
        }
        return null;
    }

    // Get tasks by priority
    public List<Task> getTasksByPriority(String priority) {
        return tasks.stream()
                .filter(task -> task.getPriority().equalsIgnoreCase(priority))
                .collect(Collectors.toList());
    }

    // Update a task
    public void updateTask(Task updatedTask) {
        Task existingTask = getTaskById(updatedTask.getId());

        if (existingTask != null) {
            existingTask.setTitle(updatedTask.getTitle());
            existingTask.setDescription(updatedTask.getDescription());
            existingTask.setCategories(updatedTask.getCategories());
            existingTask.setFileAttachment(updatedTask.getFileAttachment());
            existingTask.setPriority(updatedTask.getPriority());
            existingTask.setDate(updatedTask.getDate());
        }
    }

    // Get all tasks sorted by date
    public List<Task> getAllTasksSortedByDate(String sortOrder) {
        List<Task> sortedTasks = new ArrayList<>(tasks);
        Comparator<Task> comparator = Comparator.comparing(Task::getDate);

        if ("desc".equalsIgnoreCase(sortOrder)) {
            comparator = comparator.reversed();
        }

        sortedTasks.sort(comparator);
        return sortedTasks;
    }

    // Delete a task
    public void deleteTask(int taskId) {
        tasks.removeIf(task -> task.getId() == taskId);
    }
}