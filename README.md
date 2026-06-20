# AI Recruitment Assistant

## Overview

AI Recruitment Assistant is a Django-based recruitment platform that leverages Generative AI to automate resume screening, candidate evaluation, and recruiter decision-making.

The system processes candidate resumes, extracts relevant information using Gemini AI, analyzes job descriptions, calculates AI-based candidate scores, identifies skill gaps, generates interview questions, and provides hiring recommendations.

---

## Features

### Candidate Management

* Create, update, view, and delete candidates
* Upload PDF resumes
* Store candidate information in PostgreSQL

### Job Management

* Create, update, view, and delete job postings
* Process job descriptions using AI

### Resume Processing

* PDF text extraction using pypdf
* AI-powered resume parsing using Gemini
* Automatic skill extraction
* Candidate profile generation

### Job Analysis

* AI extraction of required job skills
* Job profile generation
* Structured job skill storage

### AI Candidate Evaluation

* Skill matching between candidate and job
* Automatic AI score calculation
* Candidate ranking system

### AI Recruiter Tools

* Interview question generation
* Skill gap analysis
* Candidate recommendation engine
* Recruiter dashboard

---

## Tech Stack

### Backend

* Python
* Django
* Django REST Framework

### Database

* PostgreSQL

### AI

* Google Gemini API

### Frontend

* Django Templates
* Bootstrap 5

### File Processing

* pypdf

---

## System Architecture

Resume PDF
↓
PDF Text Extraction
↓
Gemini AI
↓
CandidateProfile

Job Description
↓
Gemini AI
↓
JobProfile

Candidate Skills
VS
Job Skills
↓
AI Matching
↓
AI Score

AI Score
↓
Ranking
↓
Recommendations
↓
Interview Questions

---

## Implemented APIs

### Candidate APIs

* GET /api/candidates/
* POST /api/candidates/create/
* GET /api/candidates/<id>/
* PUT /api/candidates/<id>/update/
* DELETE /api/candidates/<id>/delete/

### Job APIs

* GET /api/jobs/
* POST /api/jobs/create/
* GET /api/jobs/<id>/
* PUT /api/jobs/<id>/update/
* DELETE /api/jobs/<id>/delete/

### Application APIs

* GET /api/applications/
* POST /api/applications/create/
* GET /api/applications/<id>/
* PUT /api/applications/<id>/update/
* DELETE /api/applications/<id>/delete/

### AI APIs

* POST /api/candidates/<id>/process-resume/
* POST /api/jobs/<id>/process-job/
* GET /api/jobs/<id>/rank-candidates/
* POST /api/applications/<id>/generate-questions/
* GET /api/applications/<id>/skill-gap/
* GET /api/applications/<id>/recommendation/
* GET /api/dashboard/

---

## Database Models

### Candidate

* Name
* Email
* Phone
* Resume

### Job

* Title
* Description
* Required Skills
* Experience

### Application

* Candidate
* Job
* Status
* AI Score

### CandidateProfile

* Candidate
* Extracted Data

### JobProfile

* Job
* Extracted Data

---

## Future Improvements

* JWT Authentication
* Role-Based Access Control
* Email Notifications
* Resume Vector Search
* Candidate Recommendation Enhancements
* Cloud Storage Integration
* Deployment with Docker

---

## Learning Outcomes

Through this project, I gained hands-on experience with:

* Django
* Django REST Framework
* PostgreSQL
* REST API Development
* File Upload Handling
* PDF Processing
* Generative AI Integration
* Prompt Engineering
* AI-Based Candidate Matching
* Full-Stack Web Development

---

## Author

Aanjaney Shukla

B.Tech Computer Engineering

Python | Django | DRF | PostgreSQL | AI Development
