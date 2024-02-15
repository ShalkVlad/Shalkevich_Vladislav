package com.Test.demo.services;

import com.Test.demo.models.Task;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

@Service
@Slf4j
public class TaskExporter {

    private final ObjectMapper objectMapper;

    // Constructor that accepts an ObjectMapper
    public TaskExporter(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public void exportTasks(List<Task> tasks, String exportPath) {
        try {
            // Create a directory for export
            Path exportDir = Paths.get(exportPath);
            if (!java.nio.file.Files.exists(exportDir)) {
                java.nio.file.Files.createDirectories(exportDir);
            }

            // Save each task to a separate JSON file
            for (Task task : tasks) {
                String jsonFileName = "task_" + task.getId() + ".json";
                Path jsonFile = exportDir.resolve(jsonFileName);
                objectMapper.writeValue(jsonFile.toFile(), task);
            }

            log.info("Task data export completed. Export directory: {}", exportPath);
        } catch (IOException e) {
            log.error("Error during task data export", e);
        }
    }
}
