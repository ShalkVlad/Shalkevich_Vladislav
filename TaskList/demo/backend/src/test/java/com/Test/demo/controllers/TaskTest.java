package com.Test.demo.controllers;

import com.Test.demo.models.Task;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.util.Collections;
import java.util.Date;

class TaskTest {

    @Test
    void testTaskConstructor() {
        // Arrange
        Task task = new Task();

        // Assert
        Assertions.assertNotNull(task.getDate());
        Assertions.assertEquals(1, task.getId());
    }

    @Test
    void testTaskParameterizedConstructor() {
        // Arrange
        String title = "Sample Title";
        String description = "Sample Description";
        String categories = "Sample Categories";
        String fileAttachment = "Sample File Attachment";

        // Act
        Task task = new Task(1, title, "", "", fileAttachment, "High");
        task.setDescription(description);
        task.setCategories(categories);

        // Assert
        Assertions.assertEquals(title, task.getTitle());
        Assertions.assertEquals(description, task.getDescription());
        Assertions.assertEquals(categories, task.getCategories());
        Assertions.assertEquals(fileAttachment, task.getFileAttachment());
        Assertions.assertEquals("High", task.getPriority());  // Assuming "High" is the expected priority
        Assertions.assertNotNull(task.getDate());
    }

    @Test
    void testTaskGettersAndSetters() {
        // Arrange
        Task task = new Task();

        // Act
        task.setTitle("Updated Title");
        task.setDescription("Updated Description");
        task.setCategories("Updated Categories");
        task.setFileAttachment("Updated File Attachment");
        task.setPriority("Low");
        Date currentDate = new Date();
        task.setDate(currentDate);
        task.setPdfAttachments(Collections.singletonList("pdfPath"));

        // Assert
        Assertions.assertEquals("Updated Title", task.getTitle());
        Assertions.assertEquals("Updated Description", task.getDescription());
        Assertions.assertEquals("Updated Categories", task.getCategories());
        Assertions.assertEquals("Updated File Attachment", task.getFileAttachment());
        Assertions.assertEquals("Low", task.getPriority());
        Assertions.assertEquals(currentDate, task.getDate());
        Assertions.assertEquals(Collections.singletonList("pdfPath"), task.getPdfAttachments());
    }
}
