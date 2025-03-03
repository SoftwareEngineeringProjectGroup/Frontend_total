# 1. "Lambda" Source Code

"Lambda" is a multi-modal AI assistant application based on a local large language model (LLM), featuring the following capabilities:
- Basic **chat** functionality
- Specific **online search** functionality
- **Image recognition** functionality
- **Nutritional and dietary** recommendation functionality

## 1.1 Back End

### 1.1.1 Ollama Download and Model Deployment

The language model used in this project (gemma:2b) is deployed on **Ollama**. Follow the steps below to **install and start** the model:

- Visit the [Ollama download page](https://ollama.com/download) to download and install **Ollama**.
- Ensure that Ollama is running on port **`11434`** on your local machine.
- **Start** the LLM model using the following command:

    ```PowerShell
    ollama run gemma2:2b
    ```

### 1.1.2 Django Back End Startup

This project uses the **Django framework** for the back end, which is tested on **Windows** (other systems are untested). **Make sure** the back end is running before starting the front end. Follow these steps to start the back end:

- Ensure that the **Python version** in your **Conda** environment is at least **3.10**, and that the current directory is set to **`../djangoProject`**.
- **Install** the dependencies:

    ```PowerShell
    pip install -r requirements.txt
    ```

- **Start** the Django development server:

    ```PowerShell
    python manage.py runserver
    ```

- If the terminal displays the following output, the back end has **started successfully**:

    ```PowerShell
    System check identified no issues (0 silenced).
    December 03, 2024 - 19:33:36
    Django version 5.1.1, using settings 'djangoProject.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
    ```

## 1.2 Front End

The front end is developed using **Node.js**, **Vue 3**, and **Element Plus**. **Ensure** that the back end services (**Django and Ollama**) are running before starting the front end. **Follow these steps to start the front end:**

- Make sure **Node.js** is installed. You can check by running the following commands:

    ```PowerShell
    node -v
    npm -v
    ```

- Navigate to the front end project directory (**`../SoftwareEngineer`**) and **install the dependencies**:

    ```PowerShell
    npm install
    ```

- Start the **Vue** development server:

    ```PowerShell
    npm run dev
    ```

- If the terminal displays the following message, Vue.js has been **successfully** started:

    ```PowerShell
    > lambda@0.0.0 dev
    > vite

    The CJS build of Vite's Node API is deprecated. See https://vitejs.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.

    VITE v5.4.8 ready in 733 ms

    ➜  Local:   http://localhost:5173/
    ➜  Network: use --host to expose
    ➜  press h + enter to show help
    ```

- Start the **Electron application window**:

    ```PowerShell
    npm start
    ```

- If the application window appears, the front end has started successfully.


# 2. Executable File Usage

- You can find the **`Lambda Setup.exe`** installation package after packaging the front end. Double-click the file and **follow the installation wizard**.
- After installation, follow the steps in the **[1.1 Back End](#11-back-end)** section to start the back end services.
