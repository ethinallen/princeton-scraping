# princeton-scraping

This guide will walk you through setting up and running the Princeton Scraping program using a Python virtual environment (venv) and installing all necessary requirements.

## Prerequisites

Ensure you have Python 3.6 or newer installed on your system. You can check your Python version by running:

```bash
python3 --version
```

## Setup

1. **Clone the Repository**: First, clone the repository to your local machine.

2. **Create a Virtual Environment**: Navigate to the root directory of the cloned repository and create a virtual environment named `venv`:

    ```bash
    python3 -m venv venv
    ```

3. **Activate the Virtual Environment**:

    - On **Windows**, run:

        ```bash
        .\venv\Scripts\Activate.ps1
        ```

    - On **macOS** and **Linux**, run:

        ```bash
        source venv/bin/activate
        ```

    You should now see `(venv)` at the beginning of your command line prompt, indicating that the virtual environment is activated.

4. **Install Requirements**: Install the required Python packages using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Program

Before running the program, ensure you have a `logs` folder in the root directory of the repository for the log files to be stored. If it doesn't exist, create it:

```bash
mkdir logs
```

To run the program, execute:

```bash
python3 main.py
```

This will start the scraping process, and progress will be logged to the `logs` directory.

## Deactivating the Virtual Environment

Once you're done, you can deactivate the virtual environment by running:

```bash
deactivate
```

This will return you to your global Python environment.