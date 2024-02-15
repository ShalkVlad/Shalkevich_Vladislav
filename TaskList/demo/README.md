# Проект "NoteBook"

Добро пожаловать в проект NoteBook! Этот проект представляет собой пример приложения на Java с использованием Spring Boot.

## Требования

- Java Development Kit (JDK) 17 или выше
- Apache Maven 3.6 или выше

## Как начать

1. **Установка JDK:**
   Убедитесь, что у вас установлена JDK версии 17 или выше. Вы можете скачать JDK [здесь](https://www.oracle.com/java/technologies/javase-downloads.html).

2. **Установка Maven:**
   Убедитесь, что у вас установлен Apache Maven версии 3.6 или выше. Вы можете скачать Maven [здесь](https://maven.apache.org/download.cgi).

3. **Настройка переменных среды:**
   Установите переменную среды `JAVA_HOME`, указывающую на вашу установленную JDK.
   ```shell
   setx JAVA_HOME "путь_к_вашей_JDK"
   ```

4. **Клонирование репозитория:**
   Клонируйте репозиторий: `git clone https://github.com/ваш_профиль/NoteBook.git`

5. **Сборка проекта:**
   Перейдите в корневую директорию проекта и выполните: `mvn clean install`

6. **Запуск приложения:**
   Запустите приложение: `mvn spring-boot:run`

7. **Запуск тестов:**
   Запустите приложение: `mvn test`

## Обзор

Проект "NoteBook" - это приложение на Spring Boot, предназначенное для управления задачами. Он позволяет пользователям загружать файлы PDF, экспортировать задачи и выполнять другие операции, связанные с задачами. Далее представлена информация о проекте.

## Содержание

- [Описание проекта](#project-description)
- [Зависимости](#dependencies)
- [Запуск проекта](#running-the-project)
- [Тестовые классы](#test-classes)
    - [MainControllerTest](#maincontrollertest)
    - [TaskExporterTest](#taskexportertest)
    - [TaskTest](#tasktest)
    - [PdfConverterTest](#pdfconvertertest)
    - [PdfProcessorTest](#pdfprocessortest)
    - [TaskServiceTest](#taskservicetest)

## Описание проекта

Проект "NoteBook" разработан на платформе Spring Boot и предназначен для управления задачами. Основные функции включают в себя загрузку файлов PDF, экспорт задач в файлы и обработку задач, такие как добавление, обновление и удаление.

## Зависимости

Проект использует следующие основные зависимости:

- Spring Boot 2.6.3
- Jakarta Servlet API 5.0.0
- JUnit Jupiter 5.8.2
- Mockito 4.0.0
- Spring Web 6.1.0
- Jackson Databind 2.15.3
- Apache PDFBox 2.0.28
- PowerMock 2.0.9
- Lombok 1.18.30
- и другие (см. файл [pom.xml](pom.xml))

## Запуск проекта

Для запуска проекта выполните следующие шаги:

1. Убедитесь, что [Maven](https://maven.apache.org/) и [JDK](https://www.oracle.com/java/technologies/javase-downloads.html) установлены в вашей среде разработки.
2. Склонируйте репозиторий проекта.
3. Перейдите в директорию проекта.
4. Выполните команду: `mvn spring-boot:run`.

Проект будет доступен по адресу [http://localhost:8080](http://localhost:8080).

## Тестовые классы

Тестовые классы предназначены для проверки правильности работы различных компонентов проекта. Вы можете запустить тесты с использованием вашей среды разработки или выполнить команду `mvn test`.

### MainControllerTest

Тестирует `MainController`, с акцентом на методе `uploadPdf`.

### TaskExporterTest

Тестирует сервис `TaskExporter`, охватывая функциональность экспорта задач.

### TaskTest

Тестирует модельный класс `Task`, включая конструкторы, геттеры и сеттеры.

### PdfConverterTest

Тестирует сервис `PdfConverter`, проверяя преобразование файла PDF в изображения.

### PdfProcessorTest

Тестирует сервисный класс `PdfProcessor`, охватывая обработку файлов PDF.

### TaskServiceTest

Тестирует сервисный класс `TaskService`, проверяя различные методы управления задачами.
```