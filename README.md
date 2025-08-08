# Azure Cost Analytics Dashboard

A modern, interactive web dashboard for analyzing Azure cloud costs and resource usage. This application provides real-time cost analytics, resource group breakdowns, and daily cost trends through a beautiful, responsive interface.

> ⚠️ **Work in Progress:** This project is currently under active development. Features, code, and documentation may change frequently.

## ✨ Features

- **Azure AD Authentication**: Secure login with your Azure credentials
- **Real-time Cost Analytics**: Live cost data from Azure Cost Management API
- **Interactive Charts**: Visual cost trends and resource group breakdowns
- **Resource Management**: View and manage Azure resource groups
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI**: Beautiful, intuitive interface with smooth animations

##  Quick Start

### Prerequisites

- Python 3.8 or higher
- Active Azure subscription
- Azure AD application registration

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GaleasAndres/azure-cost-analytics-dashboard
   cd azure-cost-analytics-dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Azure credentials**:
   - Follow the [Setup Guide](SETUP.md) to create an Azure AD application
   - Create a `.env` file with your Azure credentials

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the dashboard**:
   Open your browser and navigate to `http://localhost:5000`

## Setup Guide

For detailed setup instructions, including Azure AD application configuration, see the [Setup Guide](SETUP.md).

## Project Structure

```
azure-cost-analytics-dashboard/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── requirements.txt        # Python dependencies
├── SETUP.md              # Detailed setup guide
├── backend/
│   ├── api/
│   │   └── routes.py     # REST API endpoints
│   ├── auth/
│   │   └── azure_auth.py # Azure AD authentication
│   ├── azure/
│   │   ├── cost.py       # Cost analytics
│   │   ├── subscriptions.py
│   │   ├── resource_groups.py
│   │   └── credentials.py
│   └── models/           # Data models
├── frontend/
│   ├── index.html        # Dashboard interface
│   ├── app.js           # Frontend logic
│   └── styles.css       # Modern styling
└── README.md
```

## API Endpoints

The dashboard provides the following REST API endpoints:

- `GET /api/subscriptions` - List available Azure subscriptions
- `GET /api/resource-groups` - List resource groups for a subscription
- `GET /api/costs/summary` - Get cost summary with totals and averages
- `GET /api/costs/last-month` - Get daily cost data for the previous month
- `GET /api/costs/by-resource-group` - Get cost breakdown by resource group

## Features Overview

### Cost Analytics Dashboard
- **Total Cost**: Overview of total spending for the selected period
- **Average Daily Cost**: Daily cost trends and averages
- **Resource Group Breakdown**: Cost distribution across resource groups
- **Daily Cost Trends**: Interactive charts showing cost patterns over time

### Resource Management
- **Subscription Selection**: Choose from available Azure subscriptions
- **Resource Group List**: View all resource groups with details
- **Cost Attribution**: See which resource groups are consuming the most budget

### User Experience
- **Modern Design**: Clean, professional interface with smooth animations
- **Responsive Layout**: Works perfectly on all device sizes
- **Real-time Updates**: Live data refresh and loading states
- **Error Handling**: Graceful error messages and fallbacks

## 🔒 Security

- **Azure AD Integration**: Secure authentication using Microsoft Identity Platform
- **Session Management**: Secure session handling with Flask
- **Environment Variables**: Sensitive configuration stored in environment variables
- **HTTPS Ready**: Configured for secure production deployments

## Development

### Running in Development Mode

```bash
python app.py
```

The application will run in debug mode with auto-reload enabled.

### Testing

```bash
pytest
```

### Environment Variables

Create a `.env` file with the following variables:

```bash
AZURE_CLIENT_ID=your_azure_client_id
AZURE_TENANT_ID=your_azure_tenant_id
AZURE_CLIENT_SECRET=your_azure_client_secret
AZURE_REDIRECT_URI=http://localhost:5000/auth/callback
FLASK_SECRET_KEY=your_flask_secret_key
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Important Notes

- **Work in Progress**: This project is actively being developed
- **Azure Permissions**: Ensure your Azure AD app has the required permissions
- **Cost Data**: Some cost data may not be immediately available in Azure
- **Production Use**: This is a development version; add proper security for production

## 🆘 Support

If you encounter any issues:

1. Check the [Setup Guide](SETUP.md) for common solutions
2. Review the browser console for JavaScript errors
3. Check the Flask application logs for Python errors
4. Ensure your Azure credentials and permissions are correctly configured

---

**Built with ❤️ using Flask, Azure SDK, and modern web technologies**


