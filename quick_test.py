#!/usr/bin/env python3
"""
Quick test for matplotlib and base64 functionality
"""
import sys
import os

try:
    print("🧪 Testing matplotlib and base64 functionality...")
    
    # Test imports
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    import io
    import base64
    from scipy.stats import skew, kurtosis
    
    print("✅ All imports successful")
    
    # Test visualization creation
    fig, ax = plt.subplots(figsize=(8, 6))
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.exp(-x/10)
    ax.plot(x, y, 'b-', linewidth=2)
    ax.set_title('Test Biometric Visualization')
    ax.grid(True, alpha=0.3)
    
    # Convert to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight', 
               facecolor='white', edgecolor='none')
    buffer.seek(0)
    plot_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    data_url = f"data:image/png;base64,{plot_b64}"
    
    plt.close(fig)
    buffer.close()
    
    print("✅ Visualization creation successful")
    print(f"📊 Generated base64 data URL length: {len(data_url)}")
    print(f"🔗 Data URL prefix: {data_url[:50]}...")
    
    # Verify data URL format
    if data_url.startswith("data:image/png;base64,"):
        print("✅ Data URL format is correct")
    else:
        print("❌ Data URL format is incorrect")
        
    # Test scipy stats
    test_data = np.random.randn(100)
    test_skew = skew(test_data)
    test_kurtosis = kurtosis(test_data)
    print(f"✅ Scipy stats working - Skew: {test_skew:.4f}, Kurtosis: {test_kurtosis:.4f}")
    
    print("\n🎉 All functionality tests passed!")
    print("The backend should be able to generate visualizations correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    print("\n💡 Try installing missing packages:")
    print("   pip install matplotlib scipy numpy")
