package com.Test.demo.controllers;

import com.Test.demo.models.Task;
import com.Test.demo.services.PdfConverter;
import com.Test.demo.services.TaskService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.multipart.MultipartFile;

import java.util.Collections;

import static com.Test.demo.services.TaskService.logger;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.Mockito.*;

class MainControllerTest {

    @Mock
    private TaskService taskService;

    @Mock
    private FileService fileService;

    @Mock
    private PdfConverter pdfConverter;

    private MainController mainController;

    private MockMvc mockMvc;

    @BeforeEach
    public void setUp() {
        mainController = new MainController(taskService, fileService, pdfConverter);
        mockMvc = MockMvcBuilders.standaloneSetup(mainController).build();
    }

    @Test
    void uploadPdf_ValidPdfProvided_ReturnsOkResponse() throws Exception {
        // Arrange
        Task mockTask = new Task();
        when(taskService.getTaskById(anyInt())).thenReturn(mockTask);

        MockMultipartFile pdfFile = new MockMultipartFile("pdfFile", "test.pdf", "application/pdf", "test data".getBytes());
        when(fileService.saveFile(any(MultipartFile.class))).thenReturn("path/to/test.pdf");

        // Provide behavior for convertPdfToImages method
        when(pdfConverter.convertPdfToImages("path/to/test.pdf")).thenReturn(Collections.singletonList("image1.jpg"));

        // Act and Assert using MockMvc
        try {
            mockMvc.perform(MockMvcRequestBuilders.multipart("/uploadPdf/1").file(pdfFile))
                    .andExpect(MockMvcResultMatchers.status().isOk())
                    .andExpect(MockMvcResultMatchers.content().string("PDF successfully uploaded and converted."));
        } catch (Exception e) {
            logger.error("An error occurred during the test", e);
            throw e;
        }

        // Additional verification (similar to your existing code)
        verify(fileService, times(1)).saveFile(any(MultipartFile.class));
        verify(pdfConverter, times(1)).convertPdfToImages("path/to/test.pdf");
        verify(taskService, times(1)).getTaskById(anyInt());
    }
}
