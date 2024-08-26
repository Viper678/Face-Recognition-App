# FaceRecognition

This repository contains a Face Recognition application built using Python. The application is designed to capture images through a webcam, process them for face recognition, and store relevant data in a MongoDB database. The application leverages Flask for the backend, ensuring a smooth and responsive user experience.

## Prerequisites

Before setting up the application, ensure that you have the following dependencies installed:

1. **CMake**: A build tool that is essential for compiling certain Python packages.
2. **Node.js**: Required for managing JavaScript dependencies and front-end build processes.

### Install CMake

To install CMake, run the following command:

```bash
brew install cmake
```

### Install Node.js

If you don't have Node.js installed, you can install it using Homebrew:

```bash
brew install node
```
## Environment Setup

This project uses `pipenv` for managing dependencies and virtual environments.

### Set Up the Virtual Environment

Create a virtual environment using Python 3.10.4:

```bash
pipenv --python 3.10.4
```

### Activate the Virtual Environment

Enter the virtual environment shell:

```bash
pipenv shell
```

### Install Dependencies

Install all required dependencies:

```bash
pipenv install
```

## Running the Application

Once the environment is set up and dependencies are installed, you can run the application with the following command:

```bash
python app.py
```

This will start the Flask server, and the application will be accessible on `http://localhost:5000` by default.

## Notes

- Ensure that your MongoDB instance is running before launching the application.
- This setup assumes you are using a UNIX-based system (e.g., macOS or Linux). For Windows, equivalent commands may differ.
