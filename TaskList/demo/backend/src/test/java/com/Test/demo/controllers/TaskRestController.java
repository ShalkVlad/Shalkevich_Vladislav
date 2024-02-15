package com.Test.demo.controllers;

import com.Test.demo.models.Task;
import com.Test.demo.services.TaskService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Collections;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.mockito.Mockito.*;

class TaskRestControllerTest {

    @Mock
    private TaskService taskService;

    @InjectMocks
    private TaskRestController taskRestController;

    @BeforeEach
    void setUp() {
        // Initialize mocks
        MockitoAnnotations.openMocks(this);
    }

    // Test Case 1: Add Task
    @Test
    void testAddTask() {
        // Create a new task
        Task task = new Task();
        // The addTask method returns void, so use doNothing()
        doNothing().when(taskService).addTask(task);

        // Perform the operation
        ResponseEntity<Task> response = taskRestController.addTask(task);

        // Assert the results
        assertEquals(HttpStatus.CREATED, response.getStatusCode());
        verify(taskService, times(1)).addTask(task);
    }

    // Test Case 2: Get Task by Id
    @Test
    void testGetTaskById() {
        // Set up test data
        int taskId = 1;
        Task task = new Task();
        when(taskService.getTaskById(taskId)).thenReturn(task);

        // Perform the operation
        ResponseEntity<Task> response = taskRestController.getTaskById(taskId);

        // Assert the results
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(task, response.getBody());
    }

    // Test Case 3: Update Task
    @Test
    void testUpdateTask() {
        // Set up test data
        int taskId = 1;
        Task updatedTask = new Task();
        Task existingTask = new Task();
        when(taskService.getTaskById(taskId)).thenReturn(existingTask);

        // Perform the operation
        ResponseEntity<Task> response = taskRestController.updateTask(taskId, updatedTask);

        // Assert the results
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(updatedTask, response.getBody());
        verify(taskService, times(1)).updateTask(updatedTask);
    }

    // Test Case 4: Update Task Not Found
    @Test
    void testUpdateTask_NotFound() {
        // Set up test data
        int taskId = 1;
        Task updatedTask = new Task();
        when(taskService.getTaskById(taskId)).thenReturn(null);

        // Perform the operation
        ResponseEntity<Task> response = taskRestController.updateTask(taskId, updatedTask);

        // Assert the results
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        assertNull(response.getBody());
        verify(taskService, never()).updateTask(updatedTask);
    }

    // Test Case 5: Delete Task
    @Test
    void testDeleteTask() {
        // Set up test data
        int taskId = 1;
        Task task = new Task();
        when(taskService.getTaskById(taskId)).thenReturn(task);

        // Perform the operation
        ResponseEntity<Void> response = taskRestController.deleteTask(taskId);

        // Assert the results
        assertEquals(HttpStatus.NO_CONTENT, response.getStatusCode());
        verify(taskService, times(1)).deleteTask(taskId);
    }

    // Test Case 6: Delete Task Not Found
    @Test
    void testDeleteTask_NotFound() {
        // Set up test data
        int taskId = 1;
        when(taskService.getTaskById(taskId)).thenReturn(null);

        // Perform the operation
        ResponseEntity<Void> response = taskRestController.deleteTask(taskId);

        // Assert the results
        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
        verify(taskService, never()).deleteTask(taskId);
    }

    // Test Case 7: Get Tasks by Priority
    @Test
    void testGetTasksByPriority() {
        // Set up test data
        String priority = "HIGH";
        List<Task> tasks = Collections.singletonList(new Task());
        when(taskService.getTasksByPriority(priority)).thenReturn(tasks);

        // Perform the operation
        ResponseEntity<List<Task>> response = taskRestController.getTasksByPriority(priority);

        // Assert the results
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(tasks, response.getBody());
        verify(taskService, times(1)).getTasksByPriority(priority);
    }

    // Test Case 8: Get All Tasks
    @Test
    void testGetAllTasks() {
        // Set up test data
        String sort = "asc";
        List<Task> tasks = Collections.singletonList(new Task());
        when(taskService.getAllTasksSortedByDate(sort)).thenReturn(tasks);

        // Perform the operation
        ResponseEntity<List<Task>> response = taskRestController.getAllTasks(sort);

        // Assert the results
        assertEquals(HttpStatus.OK, response.getStatusCode());
        assertEquals(tasks, response.getBody());
        verify(taskService, times(1)).getAllTasksSortedByDate(sort);
    }

    // Test Case 9: Import Task with Empty Zip File
    @Test
    void testImportTask_EmptyZipFile() {
        // Set up test data
        MultipartFile zipFile = mock(MultipartFile.class);
        when(zipFile.isEmpty()).thenReturn(true);

        // Perform the operation
        ResponseEntity<String> response = taskRestController.importTask(zipFile);

        // Assert the results
        assertEquals(HttpStatus.BAD_REQUEST, response.getStatusCode());
        assertEquals("ZIP file is empty", response.getBody());
        verify(taskService, never()).addTask(any(Task.class));
    }

    // Test Case 10: Import Task with IOException
    @Test
    void testImportTask_IOException() throws IOException {
        // Set up test data
        MultipartFile zipFile = mock(MultipartFile.class);
        when(zipFile.isEmpty()).thenReturn(false);
        when(zipFile.getOriginalFilename()).thenReturn("test.zip");
        when(zipFile.getInputStream()).thenThrow(new IOException("Simulated IOException"));

        // Perform the operation
        ResponseEntity<String> response = taskRestController.importTask(zipFile);

        // Assert the results
        assertEquals(HttpStatus.INTERNAL_SERVER_ERROR, response.getStatusCode());
        assertEquals("Error importing task", response.getBody());
        verify(taskService, never()).addTask(any(Task.class));
    }
}
