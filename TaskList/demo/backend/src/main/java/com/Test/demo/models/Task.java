package com.Test.demo.models;

import lombok.Getter;
import lombok.Setter;

import java.util.Date;
import java.util.List;

@Setter
@Getter
public class Task {

    // List of PDF attachments associated with the task
    private List<String> pdfAttachments;

    // Unique identifier for the task
    private int id;

    // Title of the task
    private String title;

    // Description of the task
    private String description;

    // Categories associated with the task
    private String categories;

    // File attachment related to the task
    private String fileAttachment;

    // Priority level of the task
    private String priority;

    // Date associated with the task (creation or last update)
    private Date date;

    // Flag indicating whether the task is completed or not
    private boolean completed;

    // Constructor with parameters
    public Task(int id, String title, String description, String categories, String fileAttachment, String priority) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.categories = categories;
        this.fileAttachment = fileAttachment;
        this.priority = priority;
        this.date = new Date();
        this.completed = false;
    }

    // Default constructor with predefined values
    public Task() {
        this(1, "Sample Task 1", "", "", "", "");
    }
}