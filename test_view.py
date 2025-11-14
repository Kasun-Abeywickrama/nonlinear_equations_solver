from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def test_calculate(request):
    """Simple test endpoint"""
    try:
        data = json.loads(request.body)
        print(f"Received data: {data}")
        
        # Simple response
        response_data = {
            'root': 2.0,
            'iterations': 1,
            'error': 0.0,
            'converged': True,
            'method_name': 'Test Method',
            'execution_time': 0.001,
            'iteration_history': []
        }
        
        print(f"Sending response: {response_data}")
        return JsonResponse(response_data)
        
    except Exception as e:
        print(f"Error in test_calculate: {e}")
        return JsonResponse({'error': str(e)}, status=500)