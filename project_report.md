# E-commerce Sales Chatbot - Project Report

## 1. Project Overview
This project is a full-stack e-commerce chatbot platform designed to enhance the shopping experience by enabling users to search, explore, and simulate purchases of products via a conversational interface. The system is built with a modern, modular architecture, featuring a React frontend and a Python Flask backend, with JWT-based authentication and a mock inventory of 100+ products.

---

## 2. Architecture Overview

### High-Level Diagram
- **Frontend (React + TailwindCSS):**
  - Responsive UI for desktop, tablet, and mobile
  - Chatbot interface with session management, chat history, and product visualization
  - Login and registration with JWT session management
  - Product explorer with search and filter
- **Backend (Flask + SQLAlchemy + JWT):**
  - RESTful API for authentication, product search, and chat
  - SQLite database with 100+ mock products
  - JWT-based authentication and session management
  - Simple keyword-based chatbot logic

### Component Diagram
- **Frontend:**
  - `App.js`: Routing and context
  - `AuthContext.js`: Auth/session management
  - `pages/`: Login, Register, Chatbot, Products
- **Backend:**
  - `app.py`: App factory, blueprint registration
  - `models.py`: User and Product models
  - `auth.py`: Auth endpoints
  - `products.py`: Product endpoints
  - `chat.py`: Chatbot endpoint
  - `seed_db.py`: Database seeding

---

## 3. Technology Stack & Rationale

- **Frontend:**
  - **React:** Component-based, fast, and widely adopted for SPAs
  - **TailwindCSS:** Utility-first CSS for rapid, responsive design
  - **Axios:** Promise-based HTTP client for API calls
  - **React Router:** Declarative routing for SPA navigation
- **Backend:**
  - **Flask:** Lightweight, modular, and easy to extend for REST APIs
  - **Flask-JWT-Extended:** Secure, stateless authentication
  - **Flask-SQLAlchemy:** ORM for easy database management
  - **Flask-CORS:** Cross-origin resource sharing for frontend-backend integration
  - **Flask-Migrate:** Database migrations management
  - **SQLite:** Simple, file-based RDBMS for mock/demo data
- **Design Patterns:**
  - **Blueprints (Flask):** Modular separation of API concerns
  - **Context (React):** Centralized auth/session state
  - **Separation of Concerns:** Clear split between UI, API, and data layers

---

## 4. API Endpoints

- `POST /api/auth/register` — Register a new user
- `POST /api/auth/login` — Login and receive JWT
- `GET /api/products` — List/search products (supports `search` and `category` query params)
- `POST /api/chat` — Send a message to the chatbot (JWT required)

---

## API Documentation (Swagger)

Interactive API documentation is available via Swagger UI:

- Visit: `http://localhost:5000/apidocs/`
- For protected endpoints (e.g., /api/chat), click the "Authorize" button and enter your JWT token as:
  ```
  Bearer <your-access-token>
  ```

## 5. Sample Queries & Results

- **"Show me electronics"**
  - Returns a list of products in the Electronics category
- **"Find books under $50"**
  - (Can be extended: currently, search by keyword 'books')
- **"What is Product 10?"**
  - Returns details for Product 10 if it exists

---

## 6. Challenges & Solutions

- **Session Management:**
  - Used JWT for stateless, secure sessions; React context for client-side state
- **Mock Data Generation:**
  - Automated script (`seed_db.py`) to generate 100+ products with random categories, prices, and stock
- **Chatbot Logic:**
  - Implemented simple keyword-based search for demo; can be extended with NLP or LLMs
- **Responsive UI:**
  - TailwindCSS enabled rapid, mobile-friendly design
- **Error Handling:**
  - User feedback for login errors, API failures, and empty search results

---

## 7. Learnings & Key Takeaways

- **Modular codebase** enables easy extension (e.g., add payment, real NLP, analytics)
- **Separation of concerns** between backend API and frontend UI improves maintainability
- **Importance of user feedback** in chat interfaces for a smooth UX
- **JWT and context** provide robust, scalable session management

---

## 8. Setup & Execution Instructions

### Backend
1. `cd backend`
2. Create and activate a virtual environment
3. `pip install -r requirements.txt`
4. `flask db upgrade` (to initialize the database schema)
5. `python seed_db.py` (to seed the database)
6. `flask run`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm start`

### Usage
- Register a new user, login, and start chatting or exploring products.
- All chat and product interactions are stored for session continuity.

---

## 9. Presentation Summary

- **Objective:** Build a user-centric e-commerce chatbot for product search and purchase simulation
- **Approach:** Modular, full-stack solution with modern frameworks and best practices
- **Results:** Responsive, secure, and extensible platform with a clean codebase and clear documentation
- **Learnings:** Emphasized modularity, user experience, and robust session management

---

## 10. Screenshots & Demo
