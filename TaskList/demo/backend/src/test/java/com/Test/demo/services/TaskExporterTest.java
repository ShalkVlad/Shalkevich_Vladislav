package com.Test.demo.services;

import com.Test.demo.models.Task;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.assertTrue;

public class TaskExporterTest {

    private TaskExporter taskExporter;

    @Before
    public void setUp() {
        // Create an ObjectMapper instance
        ObjectMapper objectMapper = new ObjectMapper();
        taskExporter = new TaskExporter(objectMapper);
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
}
