
# Kid & Doctor API - README

## Overview

This API is designed to manage interactions between doctors and kids, including media uploads, voice recordings, and feedback.

---

## Swagger Documentation

**URL:** `/swagger/`

**Description:** Provides interactive API documentation.

---

## Doctor Account Management

### 1. Doctor Registration

**URL:** `/doctor/register/`

**Method:** `POST`  

**Description:** Register a new doctor.

**Request Body (JSON):**
```json
{
  "job_id": 12345,
  "phone": 987654321,
  "email": "doctor@example.com",
  "dob": "1980-01-01",
  "full_name": "Dr. John Doe"
}
```

**Success Response:**
```json
{
  "status": true,
  "message": "Doctor created successfully.",
  "data": {
    "job_id": 12345,
    "phone": 987654321,
    "email": "doctor@example.com",
    "dob": "1980-01-01",
    "full_name": "Dr. John Doe"
  }
}
```

**Error Response:**
```json
{
  "status": false,
  "message": "Error creating doctor.",
  "data": {
    "email": ["This email is already in use."]
  }
}
```

---

### 2. Doctor Login

**URL:** `/doctor/login/`

**Method:** `POST`  

**Description:** Log in an existing doctor using their `job_id`.

**Request Body (JSON):**
```json
{
  "job_id": 12345
}
```

**Success Response:**
```json
{
  "status": true,
  "message": "Login successful.",
  "data": {
    "job_id": 12345,
    "phone": 987654321,
    "email": "doctor@example.com",
    "dob": "1980-01-01",
    "full_name": "Dr. John Doe"
  }
}
```

**Error Response:**
```json
{
  "status": false,
  "message": "Doctor with job_id not found."
}
```

---

## Kid Account Management

### 3. Kid Registration

**URL:** `/kid/register/`

**Method:** `POST`  

**Description:** Register a new kid.

**Request Body (JSON):**
```json
{
  "k_id": 54321,
  "name": "Kid Name",
  "dob": "2010-06-15",
  "phone": 123456789,
  "age": 14,
  "doctor": 1
}
```

**Success Response:**
```json
{
  "status": true,
  "message": "Kid created successfully.",
  "data": {
    "k_id": 54321,
    "name": "Kid Name",
    "dob": "2010-06-15",
    "phone": 123456789,
    "age": 14,
    "doctor": 1
  }
}
```

**Error Response:**
```json
{
  "status": false,
  "message": "Error creating kid.",
  "data": {
    "phone": ["This phone is already in use."]
  }
}
```

---

### 4. Kid Login

**URL:** `/kid/login/`

**Method:** `POST`  

**Description:** Log in a kid using their `k_id`.

**Request Body (JSON):**
```json
{
  "k_id": 54321
}
```

**Success Response:**
```json
{
  "status": true,
  "message": "Login successful.",
  "data": {
    "k_id": 54321,
    "name": "Kid Name",
    "dob": "2010-06-15",
    "phone": 123456789,
    "age": 14,
    "doctor": 1
  }
}
```

**Error Response:**
```json
{
  "status": false,
  "message": "Kid with k_id not found."
}
```

---

## Profile Editing

### 5. Edit Doctor Profile

**URL:** `/doctor/edit/<str:job_id>`  
**Method:** `PUT`  
**Description:** Edit a doctor's profile.

**Request Body (JSON):**
```json
{
  "phone": 987654321,
  "email": "newemail@example.com"
}
```

**Success Response:**
```json
{
  "status": true,
  "message": "Doctor profile updated successfully.",
  "data": {
    "job_id": 12345,
    "phone": 987654321,
    "email": "newemail@example.com"
  }
}
```

---

### 6. Edit Kid Profile

**URL:** `/kid/edit/<str:k_id>`  
**Method:** `PUT`  
**Description:** Edit a kid's profile.

**Request Body (JSON):**
```json
{
  "name": "Updated Kid Name"
}
```

**Success Response:**
```json
{
  "status": true,
  "message": "Kid profile updated successfully.",
  "data": {
    "k_id": 54321,
    "name": "Updated Kid Name",
    "age": 14
  }
}
```

---

## Doctor-Kid Interaction

### 7. List Kids for a Doctor

**URL:** `/doctor/kids/`  
**Method:** `POST`  
**Description:** List all kids assigned to a specific doctor.

**Request Body (JSON):**
```json
{
  "job_id": 12345
}
```

**Success Response:**
```json
{
  "status": true,
  "message": "Kids fetched successfully.",
  "data": [
    {
      "k_id": 54321,
      "name": "Kid Name",
      "age": 14
    }
  ]
}
```

---

### 8. List Weeks for a Kid

**URL:** `/kid/weeks/<int:kid_id>`  
**Method:** `GET`  
**Description:** List all weeks for a specific kid.

**Success Response:**
```json
{
  "status": true,
  "message": "Weeks fetched successfully.",
  "data": [
    {
      "week_number": 1
    },
    {
      "week_number": 2
    }
  ]
}
```

---

## Media Upload & Management

### 9. Upload Media

**URL:** `/media/upload/`  
**Method:** `POST`  
**Description:** Upload either 4 pictures or 1 video for a specific week.

**Request Body (Multipart Form Data):**
```json
{
  "week_id": 1,
  "file": ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg"]
}
```

**Success Response (for pictures):**
```json
{
  "status": true,
  "message": "Pictures uploaded successfully."
}
```

**Request Body (Multipart Form Data):**
```json
{
  "week_id": 1,
  "file": ["video.mp4"]
}
```

**Success Response (for video):**
```json
{
  "status": true,
  "message": "Video uploaded successfully."
}
```

---

### 10. Save Media URL

**URL:** `/media/save/`  
**Method:** `POST`  
**Description:** Save the URL for uploaded media.

**Request Body (JSON for pictures):**
```json
{
  "week": 1,
  "url": [
    "https://example.com/media/image1.jpg",
    "https://example.com/media/image2.jpg",
    "https://example.com/media/image3.jpg",
    "https://example.com/media/image4.jpg"
  ]
}
```

**Request Body (JSON for video):**
```json
{
  "week": 1,
  "url": [
    "https://example.com/media/video.mp4"
  ]
}
```

**Success Response:**
```json
{
  "status": true,
  "message": "Media saved successfully."
}
```

---

## Voice Recording Upload & Management

### 11. Upload Voice Recording

**URL:** `/voice/upload/`  
**Method:** `POST`  
**Description:** Upload a voice recording for either pictures or video for a specific week.

**Request Body (Multipart Form Data):**
```json
{
  "week_id": 1,
  "file": "voice_for_pictures.mp3",
  "media_type": "pictures"
}
```

**Success Response:**
```json
{
  "status": true,
  "message": "Voice recording uploaded successfully.",
  "data": {
    "url": "https://example.com/voice/voice_for_pictures.mp3"
  }
}
```

---

### 12. Save Voice Recording URL

**URL:** `/voice/save/`  
**Method:** `POST`  
**Description:** Save the URL for uploaded voice recordings.

**Request Body (JSON):**
```json
{
  "week": 1,
  "url": "https://example.com/voice/voice_for_pictures.mp3",
  "media_type": "pictures"
}
```

**Success Response:**
```json
{
  "status": true,
  "message": "Voice recording saved successfully."
}
```

## Doctor Feedback and Media Retrieval

### 13. Add Feedback for Voice Recording

**URL:** `/voice/feedback/<int:voice_id>`  
**Method:** `POST`  
**Description:** Add feedback for a specific voice recording.

**Request Body (JSON):**
```json
{
  "stars": 4,
  "note": "Good progress!"
}
```

**Success Response:**
```json
{
  "status": true,
  "message": "Feedback added successfully.",
  "data": {
    "voice_recording": 1,
    "stars": 4,
    "note": "Good progress!"
  }
}
```

**Error Response:**
```json
{
  "status": false,
  "message": "Feedback has already been provided for this voice recording."
}
```

---

### 14. Doctor Retrieves Voice Records for a Specific Week

**URL:** `/doctor/voice-records/`  
**Method:** `GET`  
**Description:** Retrieve all voice recordings submitted by a kid for a specific week.

**Request Params:**
- `week_id`: The ID of the week to retrieve voice recordings for.

**Request Example:**
```http
GET /doctor/voice-records/?week_id=1
```

**Success Response:**
```json
{
  "status": true,
  "message": "Voice records fetched successfully.",
  "data": [
    {
      "week": 1,
      "file": "https://example.com/voice/voice_for_pictures.mp3",
      "url": "https://example.com/voice/voice_for_pictures.mp3",
      "feedback_state": false,
      "media_type": "pictures"
    },
    {
      "week": 1,
      "file": "https://example.com/voice/voice_for_video.mp3",
      "url": "https://example.com/voice/voice_for_video.mp3",
      "feedback_state": true,
      "media_type": "video"
    }
  ]
}
```

**Error Response:**
```json
{
  "status": false,
  "message": "No voice recordings found for this week."
}
```

---

### 15. Kid Retrieves Pictures and Video for a Specific Week

**URL:** `/kid/media/`  
**Method:** `GET`  
**Description:** Retrieve all pictures and the video uploaded by the doctor for a specific week.

**Request Params:**
- `week_id`: The ID of the week to retrieve media files for.

**Request Example:**
```http
GET /kid/media/?week_id=1
```

**Success Response:**
```json
{
  "status": true,
  "message": "Media files fetched successfully.",
  "data": {
    "pictures": [
      "https://example.com/media/image1.jpg",
      "https://example.com/media/image2.jpg",
      "https://example.com/media/image3.jpg",
      "https://example.com/media/image4.jpg"
    ],
    "video": "https://example.com/media/video.mp4"
  }
}
```

**Error Response:**
```json
{
  "status": false,
  "message": "The week must contain exactly 4 pictures and 1 video."
}
```

---

## General List Views

### 16. List All Doctors

**URL:** `/doctors/`  
**Method:** `GET`  
**Description:** Retrieve a list of all registered doctors.

**Success Response:**
```json
{
  "status": true,
  "message": "Doctors fetched successfully.",
  "data": [
    {
      "job_id": 12345,
      "phone": 987654321,
      "email": "doctor@example.com",
      "dob": "1980-01-01",
      "full_name": "Dr. John Doe"
    },
    {
      "job_id": 12346,
      "phone": 987654322,
      "email": "doctor2@example.com",
      "dob": "1978-12-05",
      "full_name": "Dr. Jane Smith"
    }
  ]
}
```

---

### 17. List Feedback for a Specific Kid's Voice Recordings

**URL:** `/kid/feedback/<int:kid_id>`  
**Method:** `GET`  
**Description:** List all feedback provided for a specific kid's voice recordings.

**Success Response:**
```json
{
  "status": true,
  "message": "Feedback fetched successfully.",
  "data": [
    {
      "voice_recording": 1,
      "stars": 5,
      "note": "Excellent!"
    },
    {
      "voice_recording": 2,
      "stars": 3,
      "note": "Keep practicing."
    }
  ]
}
```

**Error Response:**
```json
{
  "status": false,
  "message": "No feedback found for this kid."
}
```
