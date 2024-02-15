package com.Test.demo.controllers;

import com.Test.demo.models.Task;
import com.Test.demo.services.TaskService;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

@RestController
@RequestMapping("/api/tasks")
public class TaskRestController {

    private final TaskService taskService;
    private static final Logger logger = LoggerFactory.getLogger(TaskRestController.class);

    @Autowired
    public TaskRestController(TaskService taskService) {
        this.taskService = taskService;
    }

    @PostMapping
    public ResponseEntity<Task> addTask(@RequestBody Task task) {
        try {
            taskService.addTask(task);
            return new ResponseEntity<>(task, HttpStatus.CREATED);
        } catch (Exception e) {
            logger.error("Error adding task", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @GetMapping("/{taskId}")
    public ResponseEntity<Task> getTaskById(@PathVariable int taskId) {
        Task task = taskService.getTaskById(taskId);
        return (task != null) ? new ResponseEntity<>(task, HttpStatus.OK) : ResponseEntity.notFound().build();
    }

    @PostMapping("/update")
    public ResponseEntity<Task> updateTask(@RequestBody Task updatedTask) {
        Task existingTask = taskService.getTaskById(updatedTask.getId());
        return getTaskResponseEntity(updatedTask, existingTask);
    }

    @GetMapping("/priority/{priority}")
    public ResponseEntity<List<Task>> getTasksByPriority(@PathVariable String priority) {
        List<Task> tasks = taskService.getTasksByPriority(priority);
        return new ResponseEntity<>(tasks, HttpStatus.OK);
    }

    @GetMapping
    public ResponseEntity<List<Task>> getAllTasks(@RequestParam(required = false, defaultValue = "asc") String sort) {
        try {
            List<Task> tasksCopy = taskService.getAllTasksSortedByDate(sort);
            return new ResponseEntity<>(tasksCopy, HttpStatus.OK);
        } catch (Exception e) {
            logger.error("Error getting all tasks", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    @PutMapping("/{taskId}")
    public ResponseEntity<Task> updateTask(@PathVariable int taskId, @RequestBody Task updatedTask) {
        Task existingTask = taskService.getTaskById(taskId);
        return getTaskResponseEntity(updatedTask, existingTask);
    }

    @DeleteMapping("/{taskId}")
    public ResponseEntity<Void> deleteTask(@PathVariable int taskId) {
        Task existingTask = taskService.getTaskById(taskId);

        if (existingTask != null) {
            try {
                taskService.deleteTask(taskId);
                return ResponseEntity.noContent().build();
            } catch (Exception e) {
                logger.error("Error deleting task", e);
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
            }
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PostMapping("/import")
    public ResponseEntity<String> importTask(@RequestParam("file") MultipartFile zipFile) {
        if (zipFile.isEmpty()) {
            return ResponseEntity.badRequest().body("ZIP file is empty");
        }

        try {
            Path importDir = Files.createTempDirectory("task_import");
            Path zipFilePath = unpackZip(zipFile, importDir);

            File jsonFile = importDir.resolve("task.json").toFile();
            ObjectMapper objectMapper = new ObjectMapper();
            Task importedTask = objectMapper.readValue(jsonFile, Task.class);

            List<String> imagePaths = getImagePaths(importDir);

            importedTask.setPdfAttachments(imagePaths);
            taskService.addTask(importedTask);

            cleanUpTempFiles(importDir);

            return ResponseEntity.ok("Task successfully imported");
        } catch (JsonProcessingException e) {
            logger.error("Error processing JSON during task import", e);
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Invalid JSON format in the task file");
        } catch (IOException e) {
            logger.error("Error importing task", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error importing task: " + e.getMessage());
        } catch (Exception e) {
            logger.error("Unexpected error during task import", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Unexpected error during task import");
        }
    }

    private ResponseEntity<Task> getTaskResponseEntity(@RequestBody Task updatedTask, Task existingTask) {
        if (existingTask != null) {
            try {
                taskService.updateTask(updatedTask);
                return ResponseEntity.ok(updatedTask);
            } catch (Exception e) {
                logger.error("Error updating task", e);
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
            }
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    private Path unpackZip(MultipartFile zipFile, Path importDir) throws IOException {
        String originalFilename = zipFile.getOriginalFilename();
        if (originalFilename == null) {
            throw new IllegalArgumentException("ZIP file name is null");
        }

        Path zipFilePath = importDir.resolve(originalFilename);
        Files.copy(zipFile.getInputStream(), zipFilePath, StandardCopyOption.REPLACE_EXISTING);

        try (ZipInputStream zipInputStream = new ZipInputStream(Files.newInputStream(zipFilePath))) {
            ZipEntry entry;
            while ((entry = zipInputStream.getNextEntry()) != null) {
                Path entryPath = importDir.resolve(entry.getName());
                Files.createDirectories(entryPath.getParent());
                Files.copy(zipInputStream, entryPath, StandardCopyOption.REPLACE_EXISTING);
                zipInputStream.closeEntry();
            }
        }
        return zipFilePath;
    }

    private List<String> getImagePaths(Path importDir) throws IOException {
        try (Stream<Path> imagePathStream = Files.walk(importDir)
                .filter(path -> !Files.isDirectory(path) && !path.endsWith("task.json"))) {
            return imagePathStream.map(Path::toString).collect(Collectors.toList());
        }
    }

    private void cleanUpTempFiles(Path importDir) throws IOException {
        try (Stream<Path> pathStream = Files.walk(importDir).sorted(Comparator.reverseOrder())) {
            pathStream.map(Path::toFile).forEach(file -> {
                if (!file.delete()) {
                    logger.warn("Failed to delete file: {}", file.getAbsolutePath());
                }
            });
        }
        Files.deleteIfExists(importDir);
    }
}
