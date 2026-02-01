import sys
sys.path.insert(0, 'backend')

from app.api.v1 import admin

print("Admin router routes:")
for route in admin.router.routes:
    if hasattr(route, 'path') and hasattr(route, 'methods'):
        print(f"  {route.path} - {list(route.methods)}")

print("\nRoutes with 'clear':")
for route in admin.router.routes:
    if hasattr(route, 'path') and 'clear' in route.path.lower():
        print(f"  {route.path} - {list(route.methods) if hasattr(route, 'methods') else 'N/A'}")
