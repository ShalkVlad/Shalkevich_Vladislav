package com.Test.demo.controllers;

import com.Test.demo.models.Task;
import com.Test.demo.services.TaskExporter;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.slf4j.Logger;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.*;

class TaskExporterTest {

    @InjectMocks
    private TaskExporter taskExporter;

    @Mock
    private Logger log;

    @Mock
    private ObjectMapper objectMapper;

    private final ByteArrayOutputStream errContent = new ByteArrayOutputStream();

    @BeforeEach
    void setUp() {
        // Initialize mocks
        MockitoAnnotations.openMocks(this);

        // Redirect standard error stream before each test
        System.setErr(new PrintStream(errContent));
    }

    @Test
    void exportTasks_FailedExportWithoutErrorMessage() {
        // Arrange
        List<Task> tasks = createSampleTasks();
        String exportPath = "testExportPath";

        // Mock the behavior of the File
        File exportDir = mock(File.class);

        // Use doReturn() for constructor call
        when(exportDir.exists()).thenReturn(false);
        when(exportDir.mkdirs()).thenReturn(false);
        when(exportDir.getAbsolutePath()).thenReturn(exportPath);

        // Act
        taskExporter.exportTasks(tasks, exportPath);
    }

    @Test
    public void testExportTasks() {
        // Create some tasks for export
        List<Task> tasks = new ArrayList<>();
        tasks.add(new Task());

        // Specify a temporary directory for the test
        String exportPath = System.getProperty("java.io.tmpdir") + File.separator + "task_export_test";

        // Export the tasks
        taskExporter.exportTasks(tasks, exportPath);

        // Check that the directory is created
        File exportDir = new File(exportPath);
        assertTrue(exportDir.exists() && exportDir.isDirectory());

        // Check that files are created for each task
        for (Task task : tasks) {
            String jsonFileName = "task_" + task.getId() + ".json";
            File jsonFile = new File(exportDir, jsonFileName);
            assertTrue(jsonFile.exists());
        }
    }


    private List<Task> createSampleTasks() {
        List<Task> tasks = new ArrayList<>();
        tasks.add(new Task(1, "Sample Task 1", "", "", "", ""));
        return tasks;
    }
}
