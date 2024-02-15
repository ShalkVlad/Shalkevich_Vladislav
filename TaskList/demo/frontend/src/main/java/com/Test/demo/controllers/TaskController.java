package com.Test.demo.controllers;

import com.Test.demo.models.Task;
import com.Test.demo.services.TaskService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

@Controller
@RequestMapping("/tasks")
public class TaskController {

    private final List<Task> tasks = new ArrayList<>();
    private final TaskService taskService;
    private static final Logger log = LoggerFactory.getLogger(TaskController.class);

    @Autowired
    public TaskController(TaskService taskService) {
        this.taskService = taskService;
    }

    @GetMapping
    public String showTasks(Model model) {
        model.addAttribute("tasks", taskService.getAllTasks());
        model.addAttribute("task", new Task(1, "Sample Task 1", "", "", "", ""));
        return "taskList";
    }

    @PostMapping("/export/{taskId}")
    public ResponseEntity<byte[]> exportTask(@PathVariable int taskId) {
        Task task = taskService.getTaskById(taskId);

        if (task == null) {
            return ResponseEntity.notFound().build();
        }

        try {
            // Create a temporary directory for saving exported files
            Path exportDir = Files.createTempDirectory("task_export");

            // Save task information to a JSON file
            File jsonFile = new File(exportDir.toFile(), "task.json");
            ObjectMapper objectMapper = new ObjectMapper();
            objectMapper.writeValue(jsonFile, task);

            // Copy images to the temporary directory
            for (String imagePath : task.getPdfAttachments()) {
                File imageFile = new File(imagePath);
                Path destination = exportDir.resolve(imageFile.getName());
                Files.copy(imageFile.toPath(), destination, StandardCopyOption.REPLACE_EXISTING);
            }

            // Create a ZIP archive
            String zipFileName = "task_export_" + UUID.randomUUID() + ".zip";
            Path zipFilePath = exportDir.resolve(zipFileName);

            try (ZipOutputStream zipOutputStream = new ZipOutputStream(Files.newOutputStream(zipFilePath))) {
                Files.walk(exportDir)
                        .filter(path -> !Files.isDirectory(path))
                        .forEach(path -> {
                            ZipEntry zipEntry = new ZipEntry(exportDir.relativize(path).toString());
                            try {
                                zipOutputStream.putNextEntry(zipEntry);
                                Files.copy(path, zipOutputStream);
                                zipOutputStream.closeEntry();
                            } catch (IOException e) {
                                log.error("Error creating ZIP archive", e);
                            }
                        });
            }

            // Read the ZIP archive into a byte array
            byte[] zipBytes = Files.readAllBytes(zipFilePath);

            // Clean up temporary files
            try {
                Files.deleteIfExists(zipFilePath);
                Files.walk(exportDir)
                        .sorted(Comparator.reverseOrder())
                        .map(Path::toFile)
                        .forEach(file -> {
                            if (!file.delete()) {
                                log.warn("Failed to delete file: {}", file.getAbsolutePath());
                            }
                        });
                Files.deleteIfExists(exportDir);
            } catch (IOException e) {
                log.error("Error deleting temporary files", e);
            }

            // Return the ZIP archive as a byte array
            return ResponseEntity.ok()
                    .contentType(MediaType.APPLICATION_OCTET_STREAM)
                    .header("Content-Disposition", "attachment; filename=" + zipFileName)
                    .body(zipBytes);
        } catch (IOException e) {
            log.error("Error exporting task", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        } catch (Exception e) {
            log.error("Unexpected error during task export", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @PostMapping("/add")
    public String addTask(@ModelAttribute Task task, Model model) {
        try {
            tasks.add(task);
            return "redirect:/tasks";
        } catch (Exception e) {
            model.addAttribute("error", "Error adding task: " + e.getMessage());
            return "taskList";
        }
    }

    @GetMapping("/search/{taskId}")
    public String searchTask(@PathVariable int taskId, Model model) {
        Task foundTask = taskService.getTaskById(taskId);

        model.addAttribute("foundTask", foundTask);
        return "taskList";
    }

    @ModelAttribute("tasks")
    public List<Task> getTasks() {
        return tasks;
    }

    @ExceptionHandler(Exception.class)
    private ResponseEntity<String> handleControllerError(Exception e) {
        log.error("Unexpected error", e);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Unexpected error: " + e.getMessage());
    }

    private List<String> getImagePaths(Path importDir) throws IOException {
        try (Stream<Path> imagePathStream = Files.walk(importDir)
                .filter(path -> !Files.isDirectory(path) && !path.endsWith("task.json"))) {
            return imagePathStream.map(Path::toString).collect(Collectors.toList());
        }
    }
}