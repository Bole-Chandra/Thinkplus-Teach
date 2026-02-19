# Thinkplus Teach | Intelligent Assignment Evaluation & Feedback Platform

An AI-powered full-stack platform for students and instructors designed to streamline the assignment submission and evaluation process. Built with a robust Django backend and a premium Glassmorphism frontend.

## 🌟 Project Overview
Thinkplus Teach is an intelligent educational tool that automates the tedious aspects of grading while ensuring academic integrity. It provides instructors with instant plagiarism analysis and students with immediate pedagogical feedback.

## 🚀 Key Features
- **Comprehensive Authentication**: 
    - Secure registration and login for both Students and Instructors.
    - Mandatory email verification and role-based access control.
- **Student Dashboard**: 
    - Real-time view of active assignments.
    - Secure submission portal supporting text and PDF uploads.
    - Personalized submission history with grade tracking and AI status updates.
- **Instructor Dashboard**: 
    - Real-time tracking of student submissions with full names and IDs.
    - Automated plagiarism risk scoring for every submission.
    - Instant AI-generated pedagogical feedback.
- **AI/ML Engine**: 
    - Advanced plagiarism detection using TF-IDF and Cosine Similarity.
    - Intelligent automated grading logic.
    - Automated feedback generation based on technical depth and originality.
- **Admin Control Center**: 
    - Specialized Django Admin interface for total data management.

## 🛠️ Technical Stack
- **Backend**: Django, Django Rest Framework (RESTful APIs).
- **Frontend**: HTML5, CSS3 (Premium Glassmorphism), Vanilla JavaScript.
- **AI Logic**: Scikit-learn (TfidfVectorizer), NumPy, PDFMiner.six (PDF processing).
- **Database**: SQLite (Development) / Relational Architecture.

## 🧠 AI/ML Integration Technicality
The intelligence of Thinkplus Teach is rooted in its ability to understand and compare textual data mathematically:
- **Vectorization (TF-IDF)**: The system converts student submissions into high-dimensional vectors, emphasizing unique and meaningful terms while downplaying common filler words.
- **Similarity Scoring (Cosine Similarity)**: By calculating the cosine of the angle between these vectors, the system provides a precise percentage of similarity between the new submission and the existing database.
- **Pedagogical Logic**: Rule-based algorithms analyze the similarity scores and word counts to generate tailored feedback that encourages better academic writing.

## 📊 Database Architecture
The project follows a highly organized relational schema:
- **Users**: Manages profiles and security credentials.
- **Assignments**: Stores academic requirements and metadata.
- **Submissions**: Links students to their work, storing AI evaluations, plagiarism scores, and instructor-viewable grades.
