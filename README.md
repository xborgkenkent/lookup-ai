## Restaurant Finder

![Screenshot 2025-05-05 135504](https://github.com/user-attachments/assets/5e631fae-8ede-48c6-882f-95ea23c07b27)

## Setup Instructions

# Clone the Repository

```bash
# Clone the repository
git clone https://github.com/xborgkenkent/lookup-ai.git

# Navigate to project directory
cd lookup-ai
```

## Backend Setup (FastAPI)

1.  **Navigate to the backend directory and create virtual environment:**

    ```bash
    cd backend
    python -m venv env
    ```

2.  **Activate the virtual environment:**

    * **On Windows:**

        ```bash
        .\env\Scripts\activate
        ```

    * **On macOS and Linux:**

        ```bash
        source env/bin/activate
        ```
3.  **After the installation completes, copy the example environment file:**

    ```bash
    cp example.env .env
    ```

4.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the FastAPI application:**

    ```bash
    uvicorn main:app --reload
    ```
## Frontend Setup (Nuxt.js)

1.  **Navigate to the frontend directory:**

    ```bash
    cd frontend
    ```

2.  **Install the Node.js dependencies:**

    ```bash
    npm install
    ```

    or

    ```bash
    yarn install
    ```

    or

    ```bash
    pnpm install
    ```

3.  **After the installation completes, copy the example environment file:**

    ```bash
    cp example.env .env
    ```

4.  **Run the Nuxt.js development server:**

    ```bash
    npm run dev
    ```

    or

    ```bash
    yarn dev
    ```

    or

    ```bash
    pnpm dev
    ```


