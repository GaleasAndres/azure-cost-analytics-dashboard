# Azure Cost Analytics Dashboard - Documentation

This directory contains the documentation for the project, covering application architecture, infrastructure, deployment strategies, and development workflows.

## 📋 Documentation Index

### 🚀 Getting Started
- **[Getting Started](getting-started.md)** - Azure AD setup, configuration, and first run

### 🏗️ Architecture & Design
- **[Application Overview](application-overview.md)** - Flask application architecture, features, and components
- **[Infrastructure Guide](infrastructure-guide.md)** - Bicep modules, folder structure, and resource organization
- **[Deployment Guide](deployment-guide.md)** - Container strategies, hosting methods, and deployment patterns

### 🔄 Development Workflow
- **[Environments & Branching](environments-and-branching.md)** - Environment strategy, branching model, and pipeline logic
- **[Development Workflow](development-workflow.md)** - Step-by-step guide for developers and contributors
- **[Cost Optimization](cost-optimization.md)** - Resource sizing, cost breakdowns, and optimization strategies

## 🎯 Learning Objectives

This project is designed to continue learning Azure techonologies and implementing DevOps practices with hands-on experience:

- **Azure Infrastructure as Code (Bicep)** - For Az-104 certification preparation
- **Multiple Hosting Strategies** - App Service, Container Instances, AKS, Container Apps
- **DevOps Best Practices** - CI/CD pipelines, environment management, monitoring
- **Cost Optimization** - Resource sizing, pricing models, and cost management
- **Production Operations** - Monitoring, logging, security, and maintenance

## 🚀 Quick Start

1. **Start with** [Getting Started](getting-started.md) to set up the application locally
2. **Read** [Application Overview](application-overview.md) to understand the Flask app
3. **Review** [Infrastructure Guide](infrastructure-guide.md) to understand the Bicep structure
4. **Follow** [Environments & Branching](environments-and-branching.md) for deployment strategy

## 📊 Project Status

**Current Phase**: Infrastructure Development  
**Active Branch**: `feature/app-service-deployment`  
**Next Milestone**: Basic App Service deployment with Bicep

## 💡 Key Concepts

### Environment Strategy
- **DEV**: Multiple hosting methods for learning and comparison
- **PROD**: Single optimized hosting method for cost efficiency

### Technology Stack
- **Backend**: Flask + Python + Azure SDK + MSAL authentication
- **Infrastructure**: Azure Bicep templates, Bash and PowerShell scripts
- **Deployment**: Docker containers + Azure services
- **Monitoring**: Application Insights + Log Analytics

---

*Last Updated: 2025-08-14*
*Project: Azure Cost Analytics Dashboard*