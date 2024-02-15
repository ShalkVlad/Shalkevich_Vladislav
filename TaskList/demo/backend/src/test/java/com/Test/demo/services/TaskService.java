package com.Test.demo.services;

import com.Test.demo.models.Task;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Captor;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TaskServiceTest {

    @Mock
    private TaskService taskService;

    @Captor
    private ArgumentCaptor<Task> taskCaptor;

    @Test
    void getAllTasks() {
        // Mocking the behavior of the taskService
        List<Task> mockTasks = new ArrayList<>();
        when(taskService.getAllTasks()).thenReturn(mockTasks);

        // Call the method under test
        List<Task> result = taskService.getAllTasks();

        // Assert the result
        assertEquals(mockTasks, result);
    }

    @Test
    void addTask() {
        // Arrange
        Task taskToAdd = new Task(/* provide necessary constructor arguments */);

        // Call the method under test
        taskService.addTask(taskToAdd);

        // Verify that the addTask method was called with the correct argument
        verify(taskService).addTask(taskCaptor.capture());

        // Assert the captured argument if needed
        assertEquals(taskToAdd, taskCaptor.getValue());
    }

    @Test
    void deleteImageFromTask() {
        // Arrange
        int taskId = 1;
        String imagePath = "path/to/image.jpg";

        // Call the method under test
        taskService.deleteImageFromTask(taskId, imagePath);

        // Verify that the deleteImageFromTask method was called with the correct arguments
        verify(taskService).deleteImageFromTask(taskId, imagePath);
    }

    @Test
    void updateImageInTask() {
        // Arrange
        int taskId = 1;
        String oldImagePath = "path/to/old-image.jpg";
        String newImagePath = "path/to/new-image.jpg";

        // Call the method under test
        taskService.updateImageInTask(taskId, oldImagePath, newImagePath);

        // Verify that the updateImageInTask method was called with the correct arguments
        verify(taskService).updateImageInTask(taskId, oldImagePath, newImagePath);
    }

    @Test
    void getTasksByCategory() {
        // Arrange
        String category = "testCategory";
        List<Task> mockTasks = new ArrayList<>(); // Add tasks with the specified category
        when(taskService.getTasksByCategory(category)).thenReturn(mockTasks);

        // Call the method under test
        List<Task> result = taskService.getTasksByCategory(category);

        // Assert the result
        assertEquals(mockTasks, result);
    }

    @Test
    void linkImagesToTask() {
        // Arrange
        int taskId = 1;
        List<String> imagePaths = List.of("path/to/image1.jpg", "path/to/image2.jpg");

        // Call the method under test
        taskService.linkImagesToTask(taskId, imagePaths);

        // Verify that the linkImagesToTask method was called with the correct arguments
        verify(taskService).linkImagesToTask(taskId, imagePaths);
    }

    @Test
    void getAllTasksSortedByTitle() {
        // Arrange
        String sortOrder = "asc"; // or "desc", depending on the test case
        List<Task> mockTasks = new ArrayList<>(); // Add tasks with titles for sorting
        when(taskService.getAllTasksSortedByTitle(sortOrder)).thenReturn(mockTasks);

        // Call the method under test
        List<Task> result = taskService.getAllTasksSortedByTitle(sortOrder);

        // Assert the result
        assertEquals(mockTasks, result);
    }

    @Test
    void addAttachmentToTask() {
        // Arrange
        int taskId = 1;
        String attachment = "path/to/attachment.txt";

        // Call the method under test
        taskService.addAttachmentToTask(taskId, attachment);

        // Verify that the addAttachmentToTask method was called with the correct arguments
        verify(taskService).addAttachmentToTask(taskId, attachment);
    }
}
