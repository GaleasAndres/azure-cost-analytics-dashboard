# backend/api/routes.py

from flask import Blueprint, jsonify, request, session
from backend.azure.cost import CostAnalyzer
from backend.azure.subscriptions import SubscriptionManager
from backend.azure.resource_groups import ResourceGroupManager
import datetime

api_bp = Blueprint("api_bp", __name__)

@api_bp.route("/hello")
def hello():
    return jsonify({"message": "Hello from /api/hello!"})

@api_bp.route("/auth/status")
def auth_status():
    """Check if user is authenticated and return user info."""
    if "user" in session and "access_token" in session:
        return jsonify({
            "authenticated": True,
            "user": session["user"]
        })
    else:
        return jsonify({
            "authenticated": False,
            "user": None
        })

@api_bp.route("/debug/cost-client")
def debug_cost_client():
    """Debug the cost management client creation."""
    try:
        subscription_id = request.args.get('subscription_id')
        if not subscription_id:
            return jsonify({"error": "subscription_id parameter is required"}), 400
        
        from azure.mgmt.costmanagement import CostManagementClient
        from backend.azure.credentials import get_flask_credential
        
        credential = get_flask_credential()
        client = CostManagementClient(credential)
        
        return jsonify({
            "success": True,
            "client_type": type(client).__name__,
            "subscription_id": subscription_id,
            "scope": f"subscriptions/{subscription_id}"
        })
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@api_bp.route("/debug/cost-query")
def debug_cost_query():
    """Debug a simple cost query."""
    try:
        subscription_id = request.args.get('subscription_id')
        if not subscription_id:
            return jsonify({"error": "subscription_id parameter is required"}), 400
        
        from azure.mgmt.costmanagement import CostManagementClient
        from backend.azure.credentials import get_flask_credential
        import datetime
        
        credential = get_flask_credential()
        client = CostManagementClient(credential)
        scope = f"subscriptions/{subscription_id}"
        
        # Simple query for last 7 days
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=7)
        
        query = {
            "type": "Usage",
            "timeframe": "Custom",
            "timePeriod": {
                "from": start_date.isoformat(),
                "to": end_date.isoformat(),
            },
            "dataset": {
                "granularity": "Daily",
                "aggregation": {"totalCost": {"name": "Cost", "function": "Sum"}},
            },
        }
        
        result = client.query.usage(scope=scope, parameters=query)
        
        return jsonify({
            "success": True,
            "columns": list(result.columns),
            "row_count": len(result.rows),
            "sample_rows": result.rows[:3] if result.rows else []
        })
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@api_bp.route("/costs/last-month")
def get_last_month_costs():
    """Get daily cost data for the previous month."""
    try:
        # For now, we'll use a default subscription ID
        # In a real app, this would come from user's session or selection
        subscription_id = request.args.get('subscription_id')
        if not subscription_id:
            return jsonify({"error": "subscription_id parameter is required"}), 400
        
        analyzer = CostAnalyzer(subscription_id)
        costs = analyzer.actual_cost_last_month()
        return jsonify({"costs": costs})
    except Exception as e:
        import traceback
        print(f"Error in get_last_month_costs: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@api_bp.route("/costs/by-resource-group")
def get_costs_by_resource_group():
    """Get cost breakdown by resource group for the previous month."""
    try:
        subscription_id = request.args.get('subscription_id')
        if not subscription_id:
            return jsonify({"error": "subscription_id parameter is required"}), 400
        
        analyzer = CostAnalyzer(subscription_id)
        costs = analyzer.cost_per_resource_group()
        return jsonify({"costs": costs})
    except Exception as e:
        import traceback
        print(f"Error in get_costs_by_resource_group: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@api_bp.route("/subscriptions")
def get_subscriptions():
    """Get list of available subscriptions."""
    try:
        manager = SubscriptionManager()
        subscriptions = manager.list_subscriptions()
        return jsonify({"subscriptions": subscriptions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/resource-groups")
def get_resource_groups():
    """Get list of resource groups for a subscription."""
    try:
        subscription_id = request.args.get('subscription_id')
        if not subscription_id:
            return jsonify({"error": "subscription_id parameter is required"}), 400
        
        manager = ResourceGroupManager(subscription_id)
        resource_groups = manager.list_resource_groups()
        return jsonify({"resource_groups": resource_groups})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route("/costs/summary")
def get_cost_summary():
    """Get a summary of costs including total, by resource group, and trends."""
    try:
        subscription_id = request.args.get('subscription_id')
        if not subscription_id:
            return jsonify({"error": "subscription_id parameter is required"}), 400
        
        analyzer = CostAnalyzer(subscription_id)
        
        # Get daily costs
        daily_costs = analyzer.actual_cost_last_month()
        
        # Get resource group costs
        rg_costs = analyzer.cost_per_resource_group()
        
        # Calculate summary statistics
        total_cost = sum(float(cost.get('Cost', 0)) for cost in daily_costs)
        avg_daily_cost = total_cost / len(daily_costs) if daily_costs else 0
        
        # Group by resource group
        rg_summary = {}
        for cost in rg_costs:
            rg_name = cost.get('resource_group', 'Unknown')
            if rg_name not in rg_summary:
                rg_summary[rg_name] = 0
            rg_summary[rg_name] += float(cost.get('cost', 0))
        
        summary = {
            "total_cost": round(total_cost, 2),
            "avg_daily_cost": round(avg_daily_cost, 2),
            "period_days": len(daily_costs),
            "resource_groups": rg_summary,
            "daily_costs": daily_costs[:10]  # Last 10 days for chart
        }
        
        return jsonify(summary)
    except Exception as e:
        import traceback
        print(f"Error in get_cost_summary: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500