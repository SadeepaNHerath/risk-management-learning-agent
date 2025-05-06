# Construction Risk Management System

A machine learning-powered risk management system for construction projects that analyzes project descriptions to identify potential risks and provides mitigation strategies.

## Features

- **Risk Analysis**: AI-powered analysis of construction project descriptions to identify potential risks
- **Risk Visualization**: Interactive radar chart visualization of different risk categories
- **Incident Logging**: Record and track safety incidents, delays, budget overruns, and other issues
- **API Access**: Full functionality available via REST API endpoints
- **Responsive UI**: User-friendly interface that works across devices

## Technology Stack

- **Backend**: Python with FastAPI
- **Frontend**: HTML, CSS, JavaScript
- **UI Framework**: Bootstrap 5
- **Visualization**: Chart.js
- **API Documentation**: Swagger UI (via FastAPI)
- **Database**: SQLite (projects.db)
- **ML Model**: Pickle-serialized model (risk_model.pkl)

## Installation

### Prerequisites

- Python 3.8 or higher
- Poetry (Python dependency management)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/construction-risk-management.git
   cd construction-risk-management
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

   Alternatively, use pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
poetry run python main.py
```

Or directly with Python:

```bash
python main.py
```

The application will start and be available at [http://localhost:8000](http://localhost:8000).

### Environment Variables

- `HOST`: Host to bind the server (default: "0.0.0.0")
- `PORT`: Port to bind the server (default: "8000")
- `DEBUG`: Enable debug mode (default: "False")

## API Endpoints

- `GET /`: Redirects to the UI
- `POST /chat`: Process user messages and return risk analysis
- `GET /info`: Get system information
- `GET /health`: Check system health status
- `GET /docs`: Interactive API documentation

## Risk Categories

The system analyzes construction projects for these risk categories:

- **Safety**: Risks related to worker safety and accident prevention
- **Delay**: Timeline and schedule risks
- **Budget Overrun**: Financial and cost-related risks
- **Quality Issue**: Construction quality and specification compliance
- **Environmental**: Environmental impact and compliance risks

## Development

### Training the Model

To retrain the model with updated data:

```bash
python train_model.py
```

### Adding New Risk Categories

To add new risk categories:

1. Update the `analyzeResponseForRisks` function in `script.js` with your new category and keywords
2. Add the category to the incident type dropdown in `index.html`
3. Update the ML model to include classification for the new category

## License

[MIT License](LICENSE)

## Author

Sadeepa Herath