# debug_utils.py
print("Starting utils debug...")

try:
    print("1. Testing basic import...")
    import utils
    print(f"   utils module: {utils}")
    print(f"   utils file: {utils.__file__}")
    
    print("2. Testing direct function access...")
    if hasattr(utils, 'fetch_flight_info'):
        print("   ✓ fetch_flight_info exists")
    else:
        print("   ✗ fetch_flight_info missing")
    
    print("3. All attributes in utils:")
    for attr in dir(utils):
        if not attr.startswith('_'):
            print(f"   - {attr}")
    
    print("4. Testing manual import...")
    exec(open('utils.py').read())
    print("   Manual exec completed")
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    print(traceback.format_exc())