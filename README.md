# Tracking Number Parsing API

This project is a FastAPI-based microservice designed to parse and validate tracking numbers from various carriers. It allows users to input tracking numbers, identifies the carrier, and provides the relevant tracking information. The service is containerized using Docker and deployed on Google Cloud Run for scalable, serverless execution.

## Features

- **Carrier Detection**: Identifies the carrier from a given tracking number.
- **Tracking Number Validation**: Validates the format and checksum of tracking numbers.
- **REST API**: Provides endpoints to interact with the service programmatically.
- **Documentation**: Interactive API documentation available via Swagger UI.
- **Dockerized**: Containerized for easy deployment.
- **Cloud-Ready**: Deployable on Google Cloud Run with CI/CD integration using GitHub Actions.

## Table of Contents

- [Getting Started](#getting-started)
- [Endpoints](#endpoints)
- [Deployment](#deployment)
- [Environment Variables](#environment-variables)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

- Python 3.9 or later
- Docker
- Google Cloud SDK (for deployment)
- Git (for version control)
- GitHub account (for CI/CD integration)

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/tracking-number-parsing-api.git
    cd tracking-number-parsing-api
    ```

2. **Install Dependencies**:
    Create a virtual environment and install the required Python packages:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Run the Application Locally**:
    Start the FastAPI server:
    ```bash
    uvicorn app.main:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`.

4. **Access API Documentation**:
    Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the Swagger UI.

## Endpoints

- `GET /status` - Check the API status.
- `GET /carriers` - Get a list of all carriers that currently have parsers.
- `POST /track` - Parse and validate a tracking number (requires input).

## Deployment

### Deploying to Google Cloud Run

1. **Build the Docker Image**:
    ```bash
    docker build -t gcr.io/[PROJECT-ID]/tracking-number-parsing-api:latest .
    ```

2. **Push the Image to Google Container Registry**:
    ```bash
    docker push gcr.io/[PROJECT-ID]/tracking-number-parsing-api:latest
    ```

3. **Deploy to Google Cloud Run**:
    ```bash
    gcloud run deploy tracking-number-parsing-api \
        --image gcr.io/[PROJECT-ID]/tracking-number-parsing-api:latest \
        --platform managed \
        --region us-central1 \
        --allow-unauthenticated
    ```

### CI/CD with GitHub Actions

This project includes a GitHub Actions workflow for automated deployment to Google Cloud Run. The workflow is triggered on every push to the `main` branch.

1. **Setup GitHub Secrets**:
    - `GCP_PROJECT_ID`: Your Google Cloud project ID.
    - `GCP_SA_KEY`: Base64 encoded JSON key for your Google Cloud service account.

2. **Push Changes to the `main` Branch**:
    The GitHub Actions workflow will automatically build and deploy your application.

## Environment Variables

- `GCP_PROJECT_ID`: Your Google Cloud Project ID.
- `GCP_SA_KEY`: Google Cloud Service Account key.

The project follows a typical FastAPI application structure:

```
.
├── app
│   ├── main.py          # Entry point for the FastAPI application
│   ├── parsers          # Directory containing carrier-specific parsers
│   └── ...              # Other application files
├── Dockerfile           # Docker configuration for containerization
├── requirements.txt     # Python dependencies
├── .github
│   └── workflows        # CI/CD pipeline configuration
│       └── ci-cd.yml
├── README.md            # Project documentation
└── ...
```

## Contributing
We welcome contributions from the community. Please follow these guidelines:

1. Fork the Repository: Click the "Fork" button at the top right of the repository page.
2. Create a New Branch: Use a meaningful name for your branch (e.g., add-new-feature).
3. Commit Your Changes: Write clear and concise commit messages (e.g., Added a new feature).
4. Push to Your Branch: Use git push origin add-new-feature.
5. Submit a Pull Request: Provide a detailed description of your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments
#### FastAPI: For providing an efficient and scalable framework for building APIs.
#### Docker: For containerizing the application, making deployment simple and consistent.
#### Google Cloud Run: For enabling scalable, serverless deployments.
#### GitHub Actions: For providing a seamless CI/CD pipeline.