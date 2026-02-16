# Project Alpha: System Architecture

## 1. High-Level Design (HLD)

Project Alpha follows a **Microservices-inspired Monolith** architecture, designed for modularity and scalability.
The system is divided into three core layers:

1.  **Ingestion Layer**: Captures raw network traffic.
2.  **Processing Layer**: Extracts features and detects anomalies using AI.
3.  **Presentation Layer**: Visualizes data via CLI and Web Dashboard.

```mermaid
graph TD
    A[Network Interface (Wi-Fi/Eth0)] -->|Raw Packets| B(Packet Sniffer)
    B -->|Scapy Packet| C{Feature Extractor}
    C -->|Vector [x1, x2, ...]| D[Autoencoder Model]
    D -->|Reconstruction Error| E{Anomaly Detector}
    
    E -->|Normal (< Threshold)| F[Discard]
    E -->|Anomaly (> Threshold)| G[Alert System]
    
    G -->|JSON Log| H[anomalies.json]
    G -->|SQL Insert| I[(ForensicDB - SQLite)]
    G -->|Rich Print| J[CLI Output]
    
    I -->|Query| K[Streamlit Dashboard]
    I -->|Query| L[PDF Reporter]
```

## 2. Core Components

### 2.1 Packet Sniffer (`sniffer.py`)
-   **Technology**: `scapy`
-   **Role**: Runs in a separate daemon thread to capture packets without blocking the main application.
-   **Concurrency**: Uses `threading.Event` for graceful shutdown.

### 2.2 Feature Extractor (`features.py`)
-   **Role**: ETL (Extract, Transform, Load) pipeline for network data.
-   **Logic**:
    -   Extracts numerical fields: `len`, `sport`, `dport`.
    -   Encodes categorical fields: `proto` (TCP/UDP/ICMP).
    -   Normalizes values to [0,1] range for Neural Network stability.

### 2.3 Autoencoder Model (`model.py` / `autoencoder.py`)
-   **Technology**: `TensorFlow` / `Keras`
-   **Architecture**:
    -   **Encoder**: Compresses input (e.g., 10 features) -> Latent Space (2 neurons).
    -   **Decoder**: Reconstructs Latent Space -> Output (10 features).
-   **Training**: Unsupervised. minimizing Mean Squared Error (MSE) on "normal" traffic.
-   **Inference**: Calculates MSE between Input and Output. High MSE = Anomaly.

### 2.4 Anomaly Detector (`detector.py`)
-   **Role**: The "Brain" of the operation.
-   ** Workflow**:
    1.  Receives packet from Sniffer.
    2.  Asks Model for prediction.
    3.  Enriches result with GeoIP (`geoip.py`).
    4.  Routes alert to DB, File, and CLI.

## 3. Data Storage

### 3.1 Forensic Database (`database.py`)
-   **Technology**: `SQLite` (File-based SQL).
-   **Schema**:
    -   `id`: Primary Key.
    -   `timestamp`: Unix epoch.
    -   `src_ip`, `dst_ip`: Network entities.
    -   `score`: The generic anomaly score.
    -   `lat`, `lon`: Geolocation data for mapping.

## 4. User Interface

### 4.1 CLI (`main.py`)
-   Uses `argparse` for command-line arguments.
-   Uses `rich` for formatting tables and alerts.

### 4.2 Dashboard (`dashboard.py`)
-   **Technology**: `Streamlit`.
-   **Features**:
    -   Auto-refreshes every 2 seconds.
    -   Reads directly from `forensics.db` (Read-Only mode) to avoid locking.
    -   Renders Map using `st.map`.
