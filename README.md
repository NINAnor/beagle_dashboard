# BEAGLE Dashboard ⭐

A modern, Streamlit dashboard for visualizing and managing device deployment metadata for the [BEAGLE project]().

## 🎯 Features

### 📊 **Dashboard Components**
- **🗺️ Map Visualization**: Interactive maps with real-time device monitoring and status tracking
- **🎵 Data Overview**: Visualize the recording activity of the devices
- **📋 Site Metadata**: Comprehensive site information and metadata management

## 🏗️ Architecture

The dashboard leverages:
- **`rclone`** to serve data from S3 storage
- **Docker Compose** for multi-service orchestration
- **Reverse proxy** with authentication for secure access

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   Dashboard     │────│ Reverse Proxy│────│   rclone    │
│   (Streamlit)   │    │   (træfik)   │    │  (S3 data)  │
└─────────────────┘    └──────────────┘    └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Access credentials for the S3 bucket

### Environment Setup

1. **Create environment file**:
```bash
cp .env.example .env
```

2. **Configure credentials in `.env`**:
```bash
AUTH_USERNAME=guest
AUTH_PASSWORD=your_password_here
```

3. **Start the dashboard**:
```bash
docker compose up
```

4. **Access the dashboard**:
   - Open your browser to `http://localhost:8085`
   - Login with the credentials from your `.env` file

## 🔧 Configuration

### Environment Variables
- `AUTH_USERNAME`: HTTP Basic Auth username
- `AUTH_PASSWORD`: HTTP Basic Auth password

### Data Sources
The dashboard connects to remote S3 storage via rclone. Configure your data paths in the `docker-compose.yml` file or create a `stack.env` for production deployments.

## 📱 Usage

### Map Dashboard
- View device locations on interactive maps
- Monitor device status and connectivity
- Filter by country, region, and deployment status

### Audio Dashboard
- Browse audio recordings by device and time
- Play audio files with secure authentication
- Export recording lists and metadata
- View audio statistics and recording frequency

### Site Metadata Dashboard
- Manage site information and device metadata
- View deployment details and configurations
- Access device images and documentation

## 🧪 Testing

Run component tests:
```bash
python test_components.py
```

## 🐳 Production Deployment

For production deployment using Portainer or similar container orchestration:

1. Use Docker secrets for credentials:
```yaml
secrets:
  htpasswd:
    file: ./htpasswd
```

2. Configure environment variables appropriately
3. Ensure proper network security and access controls

See `DEPLOYMENT.md` for detailed deployment instructions.

## 🔒 Security Notes

- Never commit credentials to version control
- Use `.env` files for local development only
- Use Docker secrets or proper secret management for production
- The reverse proxy provides an additional security layer

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with clear, descriptive messages
5. Push and create a pull request

## 👥 Acknowledgment

The dashboard has been developed by:
- [Benjamin Cretois](mailto:benjamin.cretois@nina.no) - Lead Developer
- [Francesco Frassinelli](mailto:francesco.frassinelli@nina.no) - Contributor

---

*For technical support or questions, please open an issue on the repository.*
