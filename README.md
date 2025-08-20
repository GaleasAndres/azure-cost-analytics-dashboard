# Azure Cost Analytics Dashboard

## 👋 Hey there! This is my learning journey...

I'm building this project because I wanted to practice and build something that would help me learn more about cloud technologies, infrastructure, and modern development practices. My goal is to actually experience how the *software development lifecycle* works in the real world through hands-on work — not just the coding part, but the whole picture — from having an idea to bringing it to production.

**What started as a simple task** - "Let's build something for a university project" - turned into a full-blown exploration of modern cloud development. I'm covering the complete software development lifecycle: planning, architecting, choosing technologies, coding both backend and frontend, building infrastructure, setting up CI/CD pipelines, monitoring… basically everything that is done when building software in a real company.

While, with this project, I'm covering the whole software development lifecycle, I'm mainly focusing on practicing scripting and deepening my knowledge of Cloud Technologies and DevOps practices, which is something I'm passionate about.

> This Project is a Work in progress...

## 🤔 Why I'm doing this

I wanted hands-on experience with **all the pieces** of modern cloud development:

**☁️ Azure Cloud Technologies** - because I'm passionate about the Cloud and 
Azure:
- Azure SDK and services integration 
- Azure AD authentication (OAuth 2.0)
- Multiple hosting strategies (App Service, ACI, AKS, Container Apps)
- Azure CLI and PowerShell automation
- Cost Management APIs and monitoring

**🏗️ Infrastructure as Code (IaC)** - because I love hitting the keyboard, using a terminal or writing script for doing things, over clicking around Azure Portal (which is also okay):
- Bicep templates and modules
- Resource management and organization  
- Multi-environment deployments
- Infrastructure automation scripts

**🐳 Containerization & Orchestration** - containers are everywhere, so I wanted to dive deeper:
- Docker images and multi-stage builds
- Kubernetes manifests and Helm charts
- Container registries and image management
- Production-ready containerization

**💻 Full-Stack Development** - to build something actually useful:
- **Backend**: Python Flask APIs with Azure SDK integration
- **Frontend**: Vanilla JavaScript, HTML5, CSS3 (no framework bloat)
- **Authentication**: Azure AD OAuth flow implementation
- **Data**: Real-time Azure cost analytics and visualizations

**🔄 DevOps Practices** - because deployment shouldn't be scary:
- Git branching strategies and feature workflows
- CI/CD pipelines with GitHub Actions  
- Environment management (dev/prod)
- Monitoring and observability with Application Insights
- Bash and PowerShell scripting for automation

**The goal?** To experience what it's really like working on production software - from idea to deployment to monitoring. Not just tutorials, but a real project with real costs, real decisions, and real learning.

## 🎯 What I'm Learning

- **☁️ Azure Infrastructure as Code (Bicep)** - Az-104 certification preparation with real hosting/deployments
- **🚀 Multiple Hosting Strategies** - App Service, Container Instances, AKS, Container Apps comparison
- **🔄 DevOps Best Practices** - Feature branch workflows, automated CI/CD, environment management
- **💰 Cost Optimization** - Resource sizing strategies, pricing model analysis, and budget management  
- **📊 Production Operations** - Monitoring, logging, security, and maintenance practices
- **🐳 Containerization** - Docker, registry management, and container orchestration

## ✨ Application Features

The Azure Cost Analytics Dashboard provides:

- **Azure AD Authentication** - Secure OAuth 2.0 login with Microsoft accounts
- **Multi-Subscription Support** - Access cost data across multiple Azure subscriptions  
- **Cost Trend Analysis** - Daily cost breakdowns and historical trends
- **Resource Group Analytics** - Cost attribution and resource group breakdowns
- **Interactive Dashboard** - Real-time charts and responsive design

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Flask App     │────│   Azure AD       │────│  Azure Cost Mgmt    │
│   + Frontend    │    │   Authentication │    │  API Integration    │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
         │                                               │
         └─────────────────┬─────────────────────────────┘
                           │
         ┌─────────────────┴──────────────────┐
         │        Deployment Targets          │
         ├───────────────┬────────────────────┤
         │ App Service   │ Container Apps     │
         │ AKS Cluster   │ Container Instances│
         └───────────────┴────────────────────┘
```

## 📁 Project Structure

```
azure-cost-analytics-dashboard/
├── 📚 docs/                    # Comprehensive documentation
│   ├── getting-started.md      # Setup and configuration guide
│   ├── application-overview.md # Flask app architecture
│   ├── infrastructure-guide.md # Bicep structure and modules
│   ├── deployment-guide.md     # Container and hosting strategies
│   └── environments-and-branching.md # Development workflow
│
├── 🏗️ infrastructure/         # Infrastructure as Code
│   ├── bicep/                  # Azure Bicep templates
│   │   ├── modules/           # Reusable components
│   │   └── environments/      # Environment-specific configs
│   └── scripts/               # Deployment automation
│
├── 🚀 deployments/            # Application packaging
│   ├── docker/                # Container configurations
│   ├── kubernetes/            # AKS deployment manifests
│   └── helm/                  # Helm charts for AKS
│
├── 🖥️ backend/                # Flask application
│   ├── api/                   # REST API endpoints
│   ├── auth/                  # Azure AD integration
│   └── azure/                 # Azure SDK clients
│
└── 🎨 frontend/               # Web interface
    ├── index.html             # Dashboard UI
    ├── app.js                 # Frontend logic
    └── styles.css             # Modern styling
```

## 🚀 Quick Start

### For Application Development
1. **Setup**: Follow [docs/getting-started.md](docs/getting-started.md) for Azure AD configuration
2. **Run locally**: `python app.py` to test the Flask application
3. **Architecture**: Read [docs/application-overview.md](docs/application-overview.md) to understand the codebase

### For Infrastructure Learning
1. **Infrastructure**: Review [docs/infrastructure-guide.md](docs/infrastructure-guide.md) for Bicep structure
2. **Deployments**: Explore [docs/deployment-guide.md](docs/deployment-guide.md) for hosting strategies
3. **Workflow**: Study [docs/environments-and-branching.md](docs/environments-and-branching.md) for DevOps practices

## 🌍 Environment Strategy

This project uses a **cost-optimized learning approach**:

### Development Environment
- **4 hosting methods**: App Service, ACI, AKS, Container Apps
- **Purpose**: Deeping my knowledge on different hosting methods, analyzing and comparing performance, costs, and operational complexity
- **Cost**: ~$114/month for comprehensive learning

### Production Environment  
- **1 optimized method**: App Service (chosen after dev comparison)
- **Purpose**: Cost-effective production deployment
- **Cost**: ~$171/month for production-ready hosting

## 🛠️ Technology Stack

| Layer | Technologies | Purpose |
|-------|-------------|---------|
| **Frontend** | Vanilla JS, HTML5, CSS3 | Responsive dashboard interface |
| **Backend** | Flask, Python, Azure SDK, MSAL, | API server and Azure integration |  
| **Authentication** | Azure AD OAuth 2.0 | Secure Microsoft account login |
| **Infrastructure** | Azure Bicep, Azure CLI, Azure PowerShell | Infrastructure as Code deployment |
| **Containers** | Docker, Gunicorn | Application packaging and production server |
| **Monitoring** | Application Insights, Log Analytics | Observability and performance tracking |
| **CI/CD** | GitHub Actions, Azure DevOps | Automated deployment pipelines |

## 📚 Documentation

Comprehensive documentation is available in the [docs/](docs/) directory:

- **[Getting Started](docs/getting-started.md)** - Azure AD setup and configuration
- **[Application Overview](docs/application-overview.md)** - Flask app architecture and features  
- **[Infrastructure Guide](docs/infrastructure-guide.md)** - Bicep modules and resource organization
- **[Deployment Guide](docs/deployment-guide.md)** - Container strategies and hosting methods
- **[Environments & Branching](docs/environments-and-branching.md)** - Development workflow and CI/CD

## 💡 Key Learning Outcomes

After completing this project, My goal is to have deepen my knowledge, better understand the concepts and have practical experience with:

### Azure Services
- ✅ **App Service** - PaaS web hosting with deployment slots
- ✅ **Container Instances** - Serverless container hosting  
- ✅ **Kubernetes Service** - Container orchestration and advanced scaling
- ✅ **Container Apps** - Modern serverless container platform
- ✅ **Container Registry** - Private container image storage
- ✅ **Application Insights** - Application performance monitoring

### DevOps Practices  
- ✅ **Infrastructure as Code** - Bicep template development and deployment
- ✅ **CI/CD Pipelines** - Automated build, test, and deployment workflows
- ✅ **Environment Management** - Multi-environment deployment strategies
- ✅ **Cost Optimization** - Resource sizing and pricing analysis
- ✅ **Monitoring & Logging** - Production-ready observability

### Containerization
- ✅ **Docker** - Multi-stage builds and production optimizations
- ✅ **Container Orchestration** - Kubernetes manifests and Helm charts
- ✅ **Registry Management** - Image versioning and security scanning


## 💰 Cost Analysis

| Environment | Components | Monthly Cost | Learning Value |
|-------------|------------|--------------|----------------|
| **Development** | 4 hosting methods + shared resources | ~$114 | High - Compare all strategies |
| **Production** | 1 optimized method + shared resources | ~$171 | Medium - Production operations |
| **Total Project** | Complete multi-environment setup | ~$285 | **Comprehensive Azure DevOps learning** |


## 🆘 Support & Resources

- **Documentation**: Complete guides in [docs/](docs/) directory
- **Azure Learning**: Official [Azure documentation](https://docs.microsoft.com/azure/)
- **Bicep Resources**: [Azure Bicep documentation](https://docs.microsoft.com/azure/azure-resource-manager/bicep/)
- **Cost Management**: [Azure Cost Management documentation](https://docs.microsoft.com/azure/cost-management-billing/)

---

**🎓 Built for learning Azure, DevOps, and modern cloud development practices**

*This project demonstrates real-world infrastructure management, deployment strategies, and operational practices used in enterprise environments.*