# AI Recipe Management System

This is the MSE800 subject of team SLUGGO.

## Project Structure

This project is a full-stack web application with a separate front-end and back-end structure.

- **Backend Code Path**: `assignment2/ass2-api`
- **Frontend Code Path**: `assignment2/ass2-web/AI-Recipe`
- **Version Control**: The frontend project is managed using Git submodules for seamless integration.

## Prerequisites

Ensure the following are installed on your local machine before starting:

- **MySQL**: Required for the backend database.
- **Node.js & npm**: For running and building the frontend application.
- **Git**: For managing submodules and repository version control.

## Installation and Setup

### 1. Clone the Repository

Clone the repository along with its submodules using:

```bash
git clone --recurse-submodules git@github.com:pilipa-liudong/MSE800-assignment2.git
```

### 2. Setup Backend

Navigate to the backend directory and set up the backend:

```bash
cd assignment2/ass2-api
# Install dependencies
npm install
# Run database migrations and seed data (if applicable)
# Start the backend server
npm start
```

### 3. Setup Frontend

Navigate to the frontend directory and follow the instructions in its [README](assignment2/ass2-web/AI-Recipe/README.md) to set up and run the frontend.

### 4. Database Configuration

Ensure that your MySQL server is running, and update the database configuration file (e.g., `config/database.js`) with your local credentials.

## Running the Project

To run the application, start both the backend and frontend services:

- **Backend**: Verify that the backend server is connected to MySQL and running.
- **Frontend**: Refer to the [frontend README](assignment2/ass2-web/AI-Recipe/README.md) for specific instructions to start the frontend development server.

## Contributing

Contributions are welcome! Open issues or submit pull requests for any changes. Ensure that any modifications are tested and documented.

## Additional Notes

- Make sure all necessary environment variables are set before running the project (e.g., database connection strings).
- For detailed configuration or any additional dependencies for the frontend, refer to `assignment2/ass2-web/AI-Recipe/README.md`.
