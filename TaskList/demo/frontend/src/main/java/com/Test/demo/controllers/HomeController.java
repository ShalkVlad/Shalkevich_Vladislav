package com.Test.demo.controllers;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

    private static final Logger logger = LoggerFactory.getLogger(HomeController.class);

    @GetMapping("/")
    public String home() {
        try {
            logger.info("Request received for home page");
            // Your existing logic here
            return "taskList";
        } catch (Exception e) {
            logger.error("An error occurred while processing the request", e);
            // Return an error view or redirect to an error page
            return "error";
        }
    }
}
