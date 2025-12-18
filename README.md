# ReUse UMass

**Student:** Arav Mehta  
**SPIRE ID:** 34362486  
**Course:** CS 326 Web Programming  

## Project Overview
ReUse UMass is a campus reuse platform that helps students reduce waste by easily posting, browsing, and requesting free items like furniture, textbooks, and dorm essentials.

## Features
- **Browse & Filter:** View items by category (Furniture, Textbooks, etc.) or search by keyword.
- **Post Items:** Easily list new items with photos and details.
- **Request System:** Request items you need; owners receive notifications.
- **Management:** Item owners can view requests, mark items as claimed, or delete listings.
- **Authentication:** Secure login and signup system.

## Tech Stack
- **Backend:** FastAPI, SQLModel, SQLite
- **Frontend:** HTML5, CSS3, HTMX, Jinja2 Templates
- **Auth:** JWT (JSON Web Tokens), Passlib (Bcrypt)

## Setup Instructions

1. **Unzip the project** (if you haven't already).
2. **Open a terminal** in the project directory.
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   *Note: The database (`dev.db`) will be automatically created on the first run.*

2. **Open your browser**:
   Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Testing the Flow

1. **Sign Up**: Go to `/signup` (or click "Login" -> "Sign up") and create an account.
2. **Post Item**: Click "+ Post Item" and fill out the form.
3. **Browse**: Go to the home page to see your item. Try the filters.
4. **Request**: Click on an item (posted by someone else, or create a second account) and submit a request.
5. **Manage**: Go to "My Requests" to see incoming requests, mark items as claimed, or delete them.

## Knowledge Goals
The demonstration of the 10 Knowledge Goals is provided in the `knowledge_goals_demonstration.md` (or `KGD.pdf` if exported) file included in this submission.
