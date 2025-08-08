# Azure Cost Analytics Dashboard - Setup Guide

## Prerequisites

1. **Azure Account**: You need an active Azure subscription
2. **Python 3.8+**: Make sure Python is installed on your system
3. **Azure AD App Registration**: You'll need to create an Azure AD application

## Step 1: Azure AD Application Setup

### Create Azure AD App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Fill in the details:
   - **Name**: `Azure Cost Analytics Dashboard`
   - **Supported account types**: `Accounts in this organizational directory only`
   - **Redirect URI**: `Web` > `http://localhost:5000/auth/callback`
5. Click **Register**

### Configure API Permissions

1. In your app registration, go to **API permissions**
2. Click **Add a permission**
3. Select **Microsoft Graph**
4. Choose **Delegated permissions**
5. Add these permissions:
   - `User.Read` (for authentication)
   - `Directory.Read.All` (for subscription access)
6. Click **Add permissions**
7. Click **Grant admin consent**

### Get Application Credentials

1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Add a description and select expiration
4. Copy the **Value** (this is your `AZURE_CLIENT_SECRET`)
5. Go to **Overview** and copy:
   - **Application (client) ID** (this is your `AZURE_CLIENT_ID`)
   - **Directory (tenant) ID** (this is your `AZURE_TENANT_ID`)

## Step 2: Environment Configuration

1. Copy `.env.example` to `.env` (if it exists) or create a new `.env` file
2. Add your Azure credentials:

```bash
# Azure AD Application Registration
AZURE_CLIENT_ID=your_azure_client_id_here
AZURE_TENANT_ID=your_azure_tenant_id_here
AZURE_CLIENT_SECRET=your_azure_client_secret_here
AZURE_REDIRECT_URI=http://localhost:5000/auth/callback

# Flask Configuration
FLASK_SECRET_KEY=your_flask_secret_key_here
```

## Step 3: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 4: Run the Application

```bash
python app.py
```

The dashboard will be available at `http://localhost:5000`

## Step 5: First Login

1. Open your browser and go to `http://localhost:5000`
2. Click **Sign in with Azure**
3. Complete the Azure AD authentication
4. Select your subscription from the dropdown
5. View your cost analytics!

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Make sure your Azure AD app has the correct redirect URI
2. **Permission Errors**: Ensure your app has the required API permissions
3. **Cost Data Not Loading**: Verify your Azure subscription has cost data available
4. **Port Already in Use**: Change the port in `app.py` or stop other services using port 5000

### Getting Help

- Check the browser console for JavaScript errors
- Check the Flask application logs for Python errors
- Verify your Azure credentials are correct
- Ensure your Azure subscription has billing data available

## Security Notes

- Never commit your `.env` file to version control
- Use strong, unique secrets for production
- Consider using Azure Key Vault for production deployments
- Regularly rotate your Azure AD client secrets
