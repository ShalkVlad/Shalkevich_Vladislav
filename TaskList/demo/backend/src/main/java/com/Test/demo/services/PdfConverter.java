package com.Test.demo.services;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.rendering.ImageType;
import org.apache.pdfbox.rendering.PDFRenderer;
import org.springframework.stereotype.Service;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
public class PdfConverter {

    public List<String> convertPdfToImages(String pdfPath) throws IOException {
        try (PDDocument document = PDDocument.load(new File(pdfPath))) {
            PDFRenderer pdfRenderer = new PDFRenderer(document);

            List<String> imagePaths = new ArrayList<>();

            for (int page = 0; page < document.getNumberOfPages(); ++page) {
                BufferedImage bim = pdfRenderer.renderImageWithDPI(page, 300, ImageType.RGB);

                String imagePath = pdfPath.replace(".pdf", "") + "_page" + (page + 1) + ".png";
                ImageIO.write(bim, "png", new File(imagePath));

                imagePaths.add(imagePath);
            }

            return imagePaths;
        }
    }
}