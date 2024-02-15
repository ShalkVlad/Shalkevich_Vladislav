package com.Test.demo.controllers;

import com.Test.demo.models.Task;
import com.Test.demo.services.PdfConverter;
import com.Test.demo.services.TaskService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

import static com.Test.demo.services.TaskService.logger;

@RestController
@RequestMapping("/home")
public class MainController {

    private final TaskService taskService;
    private final FileService fileService;
    private final PdfConverter pdfConverter;

    @Autowired
    public MainController(TaskService taskService, FileService fileService, PdfConverter pdfConverter) {
        this.taskService = taskService;
        this.fileService = fileService;
        this.pdfConverter = pdfConverter;
    }

    @PostMapping("/uploadPdf/{taskId}")
    public Object uploadPdf(@PathVariable int taskId, @RequestParam("pdfFile") MultipartFile pdfFile) {
        try {
            Task task = taskService.getTaskById(taskId);

            if (task == null) {
                return ResponseEntity.notFound().build();
            }

            String pdfPath = fileService.saveFile(pdfFile);

            List<String> imagePaths = pdfConverter.convertPdfToImages(pdfPath);
            task.setPdfAttachments(imagePaths);

            return ResponseEntity.ok("PDF successfully uploaded and converted.");
        } catch (IOException e) {
            return handleControllerError(e, "Error processing PDF: " + e.getMessage());
        } catch (Exception e) {
            return handleControllerError(e, "Error uploading and converting PDF");
        }
    }

    private ResponseEntity<String> handleControllerError(Exception e, String errorMessage) {
        logger.error(errorMessage, e);
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Unexpected error: " + e.getMessage());
    }
}