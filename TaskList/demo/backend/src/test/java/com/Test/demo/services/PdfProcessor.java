package com.Test.demo.services;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

public class PdfProcessor {

    private static final Logger LOGGER = Logger.getLogger(PdfProcessor.class.getName());

    public List<String> convertPdfToImages(String pdfPath) throws IOException {
        // Your implementation to convert PDF to images goes here
        // For the sake of the test, let's assume it returns a list of image paths
        return List.of("image1.jpg", "image2.jpg", "image3.jpg");
    }

    public void processPdf(String pdfFilePath) {
        PDDocument document = null;

        File pdfFile = new File(pdfFilePath);
        if (!pdfFile.exists()) {
            LOGGER.log(Level.SEVERE, "The PDF file does not exist at the specified path: {0}", pdfFilePath);
        } else {
            try {
                document = PDDocument.load(pdfFile);
                // Extracting text from the PDF
                PDFTextStripper textStripper = new PDFTextStripper();
                String text = textStripper.getText(document);
                System.out.println("Text extracted from PDF:\n" + text);

                // Converting PDF to images
                List<String> imagePaths = convertPdfToImages(pdfFilePath);
                System.out.println("Images converted from PDF:\n" + imagePaths);

                // Rest of your code...
            } catch (IOException e) {
                LOGGER.log(Level.SEVERE, "Error loading or processing PDF file: {0}", e.getMessage());
                // Log the stack trace as a warning
                LOGGER.log(Level.WARNING, "Exception stack trace:", e);
            } finally {
                try {
                    if (document != null) {
                        document.close();
                    }
                } catch (IOException e) {
                    LOGGER.log(Level.SEVERE, "Error closing PDF document: {0}", e.getMessage());
                }
            }
        }
    }

    public static void main(String[] args) {
        PdfProcessor pdfProcessor = new PdfProcessor();
        pdfProcessor.processPdf("C:" + File.separator + "path" + File.separator + "to" + File.separator + "test.pdf");
    }
}
