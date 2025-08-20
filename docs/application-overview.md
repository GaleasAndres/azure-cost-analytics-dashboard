# Application Overview

## 🏗️ Architecture Summary

The Azure Cost Analytics Dashboard is a Flask-based web application that provides Azure cost monitoring and analysis through a clean, responsive interface. The application leverages Azure's Cost Management API to deliver real-time cost insights and trends.

## 📋 Application Features

### Core Functionality
- **Azure AD Authentication** - Secure OAuth 2.0 login with Microsoft accounts
- **Multi-Subscription Support** - Access cost data across multiple Azure subscriptions
- **Cost Trend Analysis** - Daily cost breakdowns and historical trends
- **Resource Group Analytics** - Cost attribution by resource group
- **Real-time Dashboard** - Interactive charts and cost summaries

### Technical Capabilities
- **Session-based Authentication** - No database required for user management
- **Azure SDK Integration** - Native Azure API connectivity
- **Responsive Design** - Works on desktop and mobile devices
- **RESTful API** - Clean API endpoints for frontend consumption

## 🎯 Application Structure

```
azure-cost-analytics-dashboard/
├── app.py                    # Main Flask application entry point
├── config.py                 # Configuration and environment variables
├── requirements.txt          # Python dependencies
│
├── backend/                  # Backend application logic
│   ├── api/                  # REST API endpoints
│   │   └── routes.py         # API route definitions
│   ├── auth/                 # Authentication handling
│   │   └── azure_auth.py     # Azure AD OAuth implementation
│   ├── azure/                # Azure service integrations
│   │   ├── cost.py           # Cost Management API client
│   │   ├── credentials.py    # Session-based credential management
│   │   ├── subscriptions.py  # Subscription management
│   │   └── resource_groups.py # Resource group operations
│   ├── models/               # Data models and structures
│   │   ├── cost_summary.py   # Cost aggregation models
│   │   ├── subscription.py   # Subscription data models
│   │   └── resource_group.py # Resource group models
│   └── utils/                # Utility functions
│       ├── errors.py         # Error handling
│       ├── logger.py         # Logging configuration
│       └── id_parser.py      # Azure resource ID parsing
│
└── frontend/                 # Frontend web interface
    ├── index.html            # Main dashboard page
    ├── app.js                # JavaScript application logic
    └── styles.css            # CSS styling
```

## 🔐 Authentication Flow

The application uses a sophisticated authentication system that bridges Flask sessions with Azure SDK credentials:

1. **User Login** → `/auth/login` redirects to Azure AD
2. **Azure Authentication** → User authenticates with Microsoft account
3. **Callback Processing** → `/auth/callback` receives authorization code
4. **Token Exchange** → Code exchanged for access token
5. **Session Storage** → Token stored in Flask session
6. **API Access** → `FlaskSessionCredential` class provides seamless Azure SDK integration

### Key Authentication Components

- **`FlaskSessionCredential`** - Custom credential provider that reads tokens from Flask sessions
- **Session Management** - Secure token storage with expiration handling
- **Scope Configuration** - Proper Azure Management API scopes for cost data access

## 🚀 API Endpoints

### Authentication Endpoints
- `GET /auth/login` - Initiate Azure AD login flow
- `GET /auth/callback` - Handle OAuth callback
- `GET /auth/logout` - Clear session and logout
- `GET /api/auth/status` - Check authentication state

### Data Endpoints
- `GET /api/subscriptions` - List user's Azure subscriptions
- `GET /api/costs/summary` - Aggregated cost data with totals
- `GET /api/costs/last-month` - Daily cost breakdown for previous month
- `GET /api/costs/by-resource-group` - Cost attribution by resource group

All data endpoints require `subscription_id` parameter and valid authentication.

## 🎨 Frontend Architecture

### Technology Stack
- **Vanilla JavaScript** - No framework dependencies for simplicity
- **Fetch API** - Modern HTTP client for API communication
- **CSS Grid/Flexbox** - Responsive layout system
- **Chart.js** (planned) - Data visualization library

### Application Flow
1. **Authentication Check** - Verify user login status
2. **Subscription Loading** - Fetch available subscriptions
3. **Subscription Selection** - User chooses target subscription
4. **Data Fetching** - Load cost data for selected subscription
5. **Visualization** - Render charts and summary cards

## 🔧 Configuration

### Environment Variables
```bash
AZURE_CLIENT_ID=<app_registration_client_id>
AZURE_TENANT_ID=<azure_tenant_id>
AZURE_CLIENT_SECRET=<app_registration_secret>
AZURE_REDIRECT_URI=http://localhost:5000/auth/callback
FLASK_SECRET_KEY=<random_secret_for_sessions>
```

### Azure AD App Registration Requirements
- **Redirect URI**: `http://localhost:5000/auth/callback`
- **Required Scopes**: 
  - `https://management.azure.com/.default`
  - `https://management.core.windows.net/.default`
- **API Permissions**: Azure Service Management API access

## 🛡️ Security Considerations

### Current Implementation
- **Secure Session Storage** - Flask sessions with secret key
- **Token Expiration Handling** - Automatic token refresh logic
- **HTTPS Redirect URIs** - Production deployment requires HTTPS
- **Scope Limitation** - Minimal required permissions for cost data

### Production Enhancements (Planned)
- **Azure Key Vault Integration** - Secure secret management
- **Managed Identity Authentication** - Eliminate client secrets
- **Rate Limiting** - API request throttling
- **Input Validation** - Enhanced request validation

## 🧪 Development & Testing

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your Azure credentials

# Run development server
python app.py
```

### Testing Strategy
- **Manual Testing** - API endpoint validation with subscription data
- **Azure AD Integration** - Authentication flow verification
- **Cost Data Accuracy** - Comparison with Azure portal cost data

## 📊 Data Flow Architecture

```
User Browser → Flask App → Azure AD (Auth) → Azure Cost Management API → Data Processing → JSON Response → Frontend Rendering
```

### Key Data Processing
- **Date Range Calculations** - Dynamic period selection (last month, custom ranges)
- **Currency Formatting** - Consistent USD formatting across all displays
- **Data Aggregation** - Resource group and daily cost summarization
- **Error Handling** - Graceful handling of API failures and missing data

---

*This overview provides the foundation for understanding the application before diving into infrastructure and deployment strategies.*