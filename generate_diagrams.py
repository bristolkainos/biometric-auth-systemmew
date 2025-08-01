"""
Comprehensive Diagram Generator for Biometric Authentication System
Generates Use Case, Data Flow, System Architecture, Algorithm Design, and Class Diagrams
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, Ellipse, Arrow
import numpy as np
import os
from datetime import datetime

# Create diagrams directory if it doesn't exist
os.makedirs('diagrams', exist_ok=True)

# Set up matplotlib for better diagram quality
plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'sans-serif'

def create_use_case_diagram():
    """Generate Use Case Diagram for Biometric Authentication System"""
    fig, ax = plt.subplots(1, 1, figsize=(20, 16))
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 18)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Title
    ax.text(12, 17.5, 'Biometric Authentication System - Use Case Diagram', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    # System boundary
    system_box = Rectangle((5, 2), 14, 14, linewidth=3, edgecolor='black', 
                          facecolor='lightblue', alpha=0.1)
    ax.add_patch(system_box)
    ax.text(12, 15.5, 'Biometric Authentication System', ha='center', va='center', 
            fontsize=14, fontweight='bold')
    
    # Actors
    # Staff User
    user_circle = Circle((2, 10), 0.7, facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(user_circle)
    ax.text(2, 8.8, 'Staff User', ha='center', va='center', fontweight='bold', fontsize=12)
    
    # Administrator
    admin_circle = Circle((2, 6), 0.7, facecolor='lightcoral', edgecolor='black', linewidth=2)
    ax.add_patch(admin_circle)
    ax.text(2, 4.8, 'Administrator', ha='center', va='center', fontweight='bold', fontsize=12)
    
    # Windows Hello System
    hello_circle = Circle((22, 12), 0.8, facecolor='lightyellow', edgecolor='black', linewidth=2)
    ax.add_patch(hello_circle)
    ax.text(22, 10.5, 'Windows Hello\nSubsystem', ha='center', va='center', fontweight='bold', fontsize=11)
    
    # NGO Secure Platform
    platform_circle = Circle((22, 6), 0.8, facecolor='lightcyan', edgecolor='black', linewidth=2)
    ax.add_patch(platform_circle)
    ax.text(22, 4.5, 'NGO Secure\nPlatform', ha='center', va='center', fontweight='bold', fontsize=11)
    
    # Primary Use Cases (Ellipses)
    use_cases = [
        (8, 13, 'Register Account\n(Multi-biometric)', 'primary'),
        (12, 13, 'Login/Authenticate\n(Password + Biometric)', 'primary'),
        (16, 13, 'Manage Account\nEnrollment', 'primary'),
        
        # Sub-processes for Register Account
        (7, 11, 'Select Biometric\nModalities', 'sub'),
        (9, 11, 'Capture Fingerprint\nSample', 'sub'),
        (11, 11, 'Capture Face\nImage', 'sub'),
        (13, 11, 'Capture Palmprint\nImage', 'sub'),
        (15, 11, 'Windows Hello\nVerification', 'sub'),
        
        # Sub-processes for Authentication
        (8, 8.5, 'Password\nVerification', 'sub'),
        (10, 8.5, 'Choose Biometric\nModality', 'sub'),
        (12, 8.5, 'Live Biometric\nCapture', 'sub'),
        (14, 8.5, 'Template\nMatching', 'sub'),
        
        # Admin functions
        (8, 5.5, 'View Registered\nUsers', 'admin'),
        (10, 5.5, 'Audit Login\nAttempts', 'admin'),
        (12, 5.5, 'Reset User\nCredentials', 'admin'),
        (14, 5.5, 'System\nConfiguration', 'admin'),
        
        # Feature extraction processes
        (16, 8.5, 'ArcFace Feature\nExtraction', 'feature'),
        (8, 3.5, 'CNN Fingerprint\nExtraction', 'feature'),
        (12, 3.5, 'CNN Palmprint\nExtraction', 'feature')
    ]
    
    for x, y, text, uc_type in use_cases:
        if uc_type == 'primary':
            color = 'white'
            width, height = 3.2, 1.2
            linewidth = 3
        elif uc_type == 'sub':
            color = 'lightgray'
            width, height = 2.5, 1.0
            linewidth = 2
        elif uc_type == 'admin':
            color = 'lightpink'
            width, height = 2.2, 1.0
            linewidth = 2
        else:  # feature
            color = 'lightyellow'
            width, height = 2.5, 1.0
            linewidth = 2
            
        ellipse = Ellipse((x, y), width, height, facecolor=color, edgecolor='black', linewidth=linewidth)
        ax.add_patch(ellipse)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold' if uc_type == 'primary' else 'normal')
    
    # Connections (Staff User to Primary Use Cases)
    staff_connections = [(8, 13), (12, 13), (16, 13)]
    for x, y in staff_connections:
        ax.plot([2.7, x-1.6], [10, y], 'k-', linewidth=2)
    
    # Connections (Admin to Admin Use Cases)
    admin_connections = [(8, 5.5), (10, 5.5), (12, 5.5), (14, 5.5), (16, 13)]
    for x, y in admin_connections:
        ax.plot([2.7, x-1.1], [6, y], 'k-', linewidth=2)
    
    # Windows Hello connections
    ax.plot([21.2, 15.8], [12, 11], 'k-', linewidth=2)
    
    # NGO Platform connection
    ax.plot([21.2, 13.6], [6, 8.5], 'k-', linewidth=2)
    
    # Include relationships (dashed lines)
    include_relationships = [
        # Register Account includes
        ((8, 13), (7, 11)),   # Select modalities
        ((8, 13), (9, 11)),   # Capture fingerprint
        ((8, 13), (11, 11)),  # Capture face
        ((8, 13), (13, 11)),  # Capture palm
        ((8, 13), (15, 11)),  # Windows Hello
        
        # Login includes
        ((12, 13), (8, 8.5)),   # Password verification
        ((12, 13), (10, 8.5)),  # Choose biometric
        ((12, 13), (12, 8.5)),  # Live capture
        ((12, 13), (14, 8.5)),  # Template matching
        
        # Feature extraction includes
        ((12, 8.5), (16, 8.5)),  # ArcFace for face
        ((9, 11), (8, 3.5)),     # CNN for fingerprint
        ((13, 11), (12, 3.5))    # CNN for palmprint
    ]
    
    for (x1, y1), (x2, y2) in include_relationships:
        ax.plot([x1, x2], [y1, y2], 'k--', linewidth=1.5, alpha=0.7)
        # Add include label
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y + 0.2, '<<include>>', ha='center', va='center', 
               fontsize=8, style='italic', rotation=0,
               bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))
    
    # Add legend
    legend_y = 1.5
    ax.text(20, 2.5, 'Legend:', ha='left', va='center', fontsize=12, fontweight='bold')
    ax.text(20, 2, 'Primary Use Cases (Bold)', ha='left', va='center', fontsize=10)
    ax.text(20, 1.7, 'Sub-processes (Gray)', ha='left', va='center', fontsize=10)
    ax.text(20, 1.4, 'Admin Functions (Pink)', ha='left', va='center', fontsize=10)
    ax.text(20, 1.1, 'AI/ML Features (Yellow)', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('diagrams/use_case_diagram.png', bbox_inches='tight', dpi=600)
    plt.close()
    print("✓ Use Case Diagram generated: diagrams/use_case_diagram.png")

def create_data_flow_diagram():
    """Generate Data Flow Diagram for Biometric Authentication System"""
    fig, ax = plt.subplots(1, 1, figsize=(24, 18))
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 20)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Title
    ax.text(15, 19.5, 'Biometric Authentication System - Data Flow Diagram (Level 1)', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    # External Entities (Squares)
    entities = [
        (3, 16, 'Staff User'),
        (27, 16, 'Administrator'),
        (3, 4, 'Windows Hello\nSubsystem'),
        (27, 4, 'NGO Secure\nPlatform')
    ]
    
    for x, y, text in entities:
        rect = Rectangle((x-1.5, y-0.7), 3, 1.4, facecolor='lightgreen', 
                        edgecolor='black', linewidth=3)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontweight='bold', fontsize=11)
    
    # Registration Processes (Upper section)
    reg_processes = [
        (8, 16, '1.0\nRegistration\nInterface'),
        (13, 16, '2.0\nBiometric\nCapture'),
        (18, 16, '3.0\nFeature\nExtraction'),
        (23, 16, '4.0\nWindows Hello\nVerification'),
        (8, 13, '5.0\nFingerprint\nCNN Model'),
        (13, 13, '6.0\nArcFace\nFace Model'),
        (18, 13, '7.0\nPalmprint\nCNN Model'),
        (23, 13, '8.0\nCredential\nStorage')
    ]
    
    # Authentication Processes (Lower section)
    auth_processes = [
        (8, 9, '9.0\nLogin\nInterface'),
        (13, 9, '10.0\nPassword\nVerification'),
        (18, 9, '11.0\nBiometric\nMatching'),
        (23, 9, '12.0\nTemplate\nComparison'),
        (8, 6, '13.0\nLive Biometric\nCapture'),
        (13, 6, '14.0\nFeature\nExtraction'),
        (18, 6, '15.0\nSimilarity\nCalculation'),
        (23, 6, '16.0\nAccess\nDecision')
    ]
    
    all_processes = reg_processes + auth_processes
    
    for x, y, text in all_processes:
        circle = Circle((x, y), 1.2, facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Data Stores (Open rectangles)
    stores = [
        (8, 2, 'D1: User Database'),
        (13, 2, 'D2: Biometric Templates'),
        (18, 2, 'D3: Password Hashes'),
        (23, 2, 'D4: Audit Logs')
    ]
    
    for x, y, text in stores:
        # Open rectangle (two parallel lines)
        ax.plot([x-2, x+2], [y+0.4, y+0.4], 'k-', linewidth=3)
        ax.plot([x-2, x+2], [y-0.4, y-0.4], 'k-', linewidth=3)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Registration Data Flows
    reg_flows = [
        # From Staff User
        ((4.5, 16), (6.8, 16), 'User Info + Password'),
        ((4.5, 15.5), (6.8, 13.5), 'Biometric Selection'),
        
        # Registration process flows
        ((9.2, 16), (11.8, 16), 'Capture Request'),
        ((14.2, 16), (16.8, 16), 'Raw Biometric Data'),
        ((19.2, 16), (21.8, 16), 'Feature Vectors'),
        
        # Biometric processing
        ((13, 14.8), (8, 14.2), 'Fingerprint Image'),
        ((13, 14.8), (13, 14.2), 'Face Image'),
        ((13, 14.8), (18, 14.2), 'Palm Image'),
        
        # Feature vectors to storage
        ((8, 11.8), (23, 14.2), 'Fingerprint Template'),
        ((13, 11.8), (23, 14.2), 'Face Embedding'),
        ((18, 11.8), (23, 14.2), 'Palm Template'),
        
        # Windows Hello verification
        ((3, 4.7), (22, 12), 'Identity Verification'),
        
        # To data stores
        ((23, 11.8), (13, 2.4), 'Store Templates'),
        ((23, 11.8), (18, 2.4), 'Store Password Hash'),
        ((23, 11.8), (8, 2.4), 'Create User Record')
    ]
    
    # Authentication Data Flows
    auth_flows = [
        # From Staff User (authentication)
        ((4.5, 15), (6.8, 9), 'Login Credentials'),
        ((4.5, 14.5), (6.8, 6), 'Live Biometric'),
        
        # Authentication process flows
        ((9.2, 9), (11.8, 9), 'Username + Password'),
        ((14.2, 9), (16.8, 9), 'Password Verified'),
        ((19.2, 9), (21.8, 9), 'Match Score'),
        
        # Live biometric processing
        ((9.2, 6), (11.8, 6), 'Live Sample'),
        ((14.2, 6), (16.8, 6), 'Live Features'),
        ((19.2, 6), (21.8, 6), 'Similarity Score'),
        
        # Database queries
        ((13, 7.8), (13, 2.4), 'Query Templates'),
        ((18, 7.8), (18, 2.4), 'Query Password'),
        
        # To NGO Platform
        ((24.2, 6), (25.5, 4.7), 'Access Token'),
        
        # Audit logging
        ((23, 7.8), (23, 2.4), 'Log Attempt')
    ]
    
    all_flows = reg_flows + auth_flows
    
    for (x1, y1), (x2, y2), label in all_flows:
        # Draw arrow
        if abs(x1 - x2) > abs(y1 - y2):  # Horizontal arrow
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', color='red', lw=2))
        else:  # Vertical arrow
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', color='blue', lw=2))
        
        # Add label
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y + 0.3, label, ha='center', va='bottom', 
               fontsize=8, bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.9))
    
    # Add section labels
    ax.text(15, 17.5, 'REGISTRATION PROCESS', ha='center', va='center', 
            fontsize=14, fontweight='bold', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcyan', alpha=0.8))
    
    ax.text(15, 10.5, 'AUTHENTICATION PROCESS', ha='center', va='center', 
            fontsize=14, fontweight='bold',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.8))
    
    # Add legend
    ax.text(1, 1, 'Data Flow Legend:', ha='left', va='center', fontsize=12, fontweight='bold')
    ax.text(1, 0.5, 'Red arrows: Registration flows', ha='left', va='center', fontsize=10, color='red')
    ax.text(1, 0.2, 'Blue arrows: Authentication flows', ha='left', va='center', fontsize=10, color='blue')
    
    plt.tight_layout()
    plt.savefig('diagrams/data_flow_diagram.png', bbox_inches='tight', dpi=600)
    plt.close()
    print("✓ Data Flow Diagram generated: diagrams/data_flow_diagram.png")

def create_system_architecture_diagram():
    """Generate System Architecture Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(28, 20))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 22)
    ax.axis('off')
    
    # Title
    ax.text(16, 21.5, 'Biometric Authentication System - System Architecture', 
            ha='center', va='center', fontsize=20, fontweight='bold')
    
    # User Interface Layer (WinUI/C#)
    ui_box = FancyBboxPatch((2, 17.5), 28, 3, boxstyle="round,pad=0.2", 
                           facecolor='lightgreen', edgecolor='black', linewidth=3)
    ax.add_patch(ui_box)
    ax.text(16, 19.8, 'USER INTERFACE LAYER (WinUI/C#)', ha='center', va='center', 
            fontsize=16, fontweight='bold')
    
    # UI components
    ui_components = [
        (5, 19, 'Registration\nInterface'),
        (9, 19, 'Login\nInterface'),
        (13, 19, 'Biometric\nCapture UI'),
        (17, 19, 'Admin\nDashboard'),
        (21, 19, 'User\nFeedback'),
        (25, 19, 'Error\nHandling'),
        (6, 18, 'Camera\nPreview'),
        (10, 18, 'Fingerprint\nSensor UI'),
        (14, 18, 'Palm Capture\nInterface'),
        (18, 18, 'Windows Hello\nPrompts'),
        (22, 18, 'Progress\nIndicators'),
        (26, 18, 'Security\nNotifications')
    ]
    
    for x, y, text in ui_components:
        rect = Rectangle((x-1, y-0.4), 2, 0.8, facecolor='white', 
                        edgecolor='green', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Sensor and Capture Layer
    sensor_box = FancyBboxPatch((2, 14), 28, 2.5, boxstyle="round,pad=0.2", 
                               facecolor='lightblue', edgecolor='black', linewidth=3)
    ax.add_patch(sensor_box)
    ax.text(16, 15.8, 'SENSOR AND CAPTURE LAYER', ha='center', va='center', 
            fontsize=16, fontweight='bold')
    
    # Sensor components
    sensors = [
        (6, 15.2, 'Fingerprint\nSensor/Camera'),
        (10, 15.2, 'Webcam\n(OpenCV)'),
        (14, 15.2, 'Windows Hello\nSensors'),
        (18, 15.2, 'Image\nPreprocessing'),
        (22, 15.2, 'Quality\nAssessment'),
        (26, 15.2, 'Liveness\nDetection'),
        (8, 14.4, 'OpenCVSharp\nIntegration'),
        (16, 14.4, 'Real-time\nCapture'),
        (24, 14.4, 'Multi-modal\nSupport')
    ]
    
    for x, y, text in sensors:
        rect = Rectangle((x-1.2, y-0.4), 2.4, 0.8, facecolor='white', 
                        edgecolor='blue', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Biometric Processing Layer (AI/ML Models)
    processing_box = FancyBboxPatch((2, 10), 28, 3, boxstyle="round,pad=0.2", 
                                   facecolor='lightyellow', edgecolor='black', linewidth=3)
    ax.add_patch(processing_box)
    ax.text(16, 12.3, 'BIOMETRIC PROCESSING LAYER (AI/ML MODELS)', ha='center', va='center', 
            fontsize=16, fontweight='bold')
    
    # Processing components
    processing = [
        (5, 11.8, 'ArcFace ONNX\n(ResNet100)'),
        (9, 11.8, 'Fingerprint CNN\n(Custom Model)'),
        (13, 11.8, 'Palmprint CNN\n(Custom Model)'),
        (17, 11.8, 'ONNX Runtime\nExecution'),
        (21, 11.8, 'Feature Vector\nExtraction'),
        (25, 11.8, 'Template\nGeneration'),
        (5, 11, 'Face Detection\n& Cropping'),
        (9, 11, 'Minutiae\nExtraction'),
        (13, 11, 'Palm Line\nDetection'),
        (17, 11, 'GPU/CPU\nAcceleration'),
        (21, 11, 'Similarity\nCalculation'),
        (25, 11, 'Threshold\nComparison'),
        (6, 10.2, 'Cosine Similarity\n(Face)'),
        (10, 10.2, 'Euclidean Distance\n(Fingerprint)'),
        (14, 10.2, 'Vector Matching\n(Palm)'),
        (18, 10.2, 'Multi-modal\nFusion'),
        (22, 10.2, 'Score\nNormalization'),
        (26, 10.2, 'Decision\nLogic')
    ]
    
    for x, y, text in processing:
        rect = Rectangle((x-1.2, y-0.3), 2.4, 0.6, facecolor='white', 
                        edgecolor='orange', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Authentication & Security Layer
    auth_box = FancyBboxPatch((2, 6.5), 28, 2.5, boxstyle="round,pad=0.2", 
                             facecolor='lightcoral', edgecolor='black', linewidth=3)
    ax.add_patch(auth_box)
    ax.text(16, 8.3, 'AUTHENTICATION & SECURITY LAYER', ha='center', va='center', 
            fontsize=16, fontweight='bold')
    
    # Authentication components
    auth_components = [
        (5, 7.8, 'Password\nHashing (BCrypt)'),
        (9, 7.8, 'Windows Hello\nIntegration'),
        (13, 7.8, 'Multi-factor\nAuthentication'),
        (17, 7.8, 'Session\nManagement'),
        (21, 7.8, 'Access\nControl'),
        (25, 7.8, 'Audit\nLogging'),
        (7, 7, 'UserConsentVerifier\nAPI'),
        (15, 7, 'Template\nEncryption'),
        (23, 7, 'Security\nPolicies')
    ]
    
    for x, y, text in auth_components:
        rect = Rectangle((x-1.2, y-0.4), 2.4, 0.8, facecolor='white', 
                        edgecolor='red', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Database & Storage Layer
    db_box = FancyBboxPatch((2, 3), 28, 2.5, boxstyle="round,pad=0.2", 
                           facecolor='lightgray', edgecolor='black', linewidth=3)
    ax.add_patch(db_box)
    ax.text(16, 4.8, 'DATABASE & SECURE STORAGE LAYER', ha='center', va='center', 
            fontsize=16, fontweight='bold')
    
    # Database components
    db_components = [
        (5, 4.3, 'SQLite/Local\nDatabase'),
        (9, 4.3, 'User\nCredentials'),
        (13, 4.3, 'Biometric\nTemplates'),
        (17, 4.3, 'Encrypted\nStorage'),
        (21, 4.3, 'Backup &\nRecovery'),
        (25, 4.3, 'Data\nIntegrity'),
        (7, 3.5, 'Password\nHashes'),
        (11, 3.5, 'Feature\nVectors'),
        (15, 3.5, 'User\nMetadata'),
        (19, 3.5, 'Audit\nTrails'),
        (23, 3.5, 'Configuration\nData'),
        (27, 3.5, 'System\nLogs')
    ]
    
    for x, y, text in db_components:
        rect = Rectangle((x-1, y-0.4), 2, 0.8, facecolor='white', 
                        edgecolor='gray', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # External Integration Layer
    ext_box = FancyBboxPatch((2, 0.5), 28, 1.5, boxstyle="round,pad=0.2", 
                            facecolor='lightcyan', edgecolor='black', linewidth=3)
    ax.add_patch(ext_box)
    ax.text(16, 1.5, 'EXTERNAL INTEGRATION LAYER', ha='center', va='center', 
            fontsize=16, fontweight='bold')
    
    # External components
    ext_components = [
        (6, 1.2, 'Windows\nSecurity APIs'),
        (12, 1.2, 'NGO Platform\nIntegration'),
        (18, 1.2, 'Hardware\nDrivers'),
        (24, 1.2, 'Admin\nInterfaces')
    ]
    
    for x, y, text in ext_components:
        rect = Rectangle((x-1.5, y-0.3), 3, 0.6, facecolor='white', 
                        edgecolor='cyan', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Add arrows between layers
    layer_arrows = [
        ((16, 17.5), (16, 16.5)),  # UI to Sensor
        ((16, 14), (16, 13)),      # Sensor to Processing
        ((16, 10), (16, 9)),       # Processing to Auth
        ((16, 6.5), (16, 5.5)),    # Auth to Database
        ((16, 3), (16, 2))         # Database to External
    ]
    
    for (x1, y1), (x2, y2) in layer_arrows:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='<->', color='black', lw=3))
    
    # Side annotations
    ax.text(0.5, 19, 'User\nInteraction', ha='center', va='center', 
            fontsize=12, fontweight='bold', rotation=90)
    ax.text(0.5, 15.2, 'Data\nCapture', ha='center', va='center', 
            fontsize=12, fontweight='bold', rotation=90)
    ax.text(0.5, 11.5, 'AI/ML\nProcessing', ha='center', va='center', 
            fontsize=12, fontweight='bold', rotation=90)
    ax.text(0.5, 7.8, 'Security\n& Auth', ha='center', va='center', 
            fontsize=12, fontweight='bold', rotation=90)
    ax.text(0.5, 4.2, 'Data\nStorage', ha='center', va='center', 
            fontsize=12, fontweight='bold', rotation=90)
    ax.text(0.5, 1.2, 'External\nSystems', ha='center', va='center', 
            fontsize=12, fontweight='bold', rotation=90)
    
    # Add technology stack annotation
    tech_text = """
Technology Stack:
• Frontend: WinUI (C#)
• Computer Vision: OpenCVSharp
• AI/ML: ONNX Runtime
• Face Recognition: ArcFace (ResNet100)
• CNNs: Custom Fingerprint & Palm Models
• Security: Windows Hello API, BCrypt
• Database: SQLite with encryption
• Platform: .NET Framework
"""
    ax.text(31, 11, tech_text, ha='left', va='center', fontsize=10,
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig('diagrams/system_architecture_diagram.png', bbox_inches='tight', dpi=600)
    plt.close()
    print("✓ System Architecture Diagram generated: diagrams/system_architecture_diagram.png")

def create_algorithm_design_diagrams():
    """Generate Algorithm Design Diagrams for Registration and Authentication"""
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(32, 20))
    
    # Registration Algorithm Flowchart
    ax1.set_xlim(0, 12)
    ax1.set_ylim(0, 24)
    ax1.axis('off')
    ax1.set_title('Registration Algorithm (RegisterUser)', fontsize=18, fontweight='bold', pad=20)
    
    # Flowchart elements for registration
    reg_steps = [
        (6, 23, 'START', 'ellipse', 'lightgreen'),
        (6, 21.5, 'Input: username, password\nselectedBiometrics[]', 'rect', 'lightblue'),
        (6, 20, 'Check if username\nexists in database', 'rect', 'lightblue'),
        (6, 18.5, 'Username\nExists?', 'diamond', 'yellow'),
        (6, 17, 'Windows Hello\nVerifyUserPresence()', 'rect', 'lightcoral'),
        (6, 15.5, 'Verification\nSuccessful?', 'diamond', 'yellow'),
        (6, 14, 'pwd_hash = HashFunction\n(password)', 'rect', 'lightblue'),
        (6, 12.5, 'Initialize empty\nuserTemplates{}', 'rect', 'lightblue'),
        (6, 11, 'For each modality in\nselectedBiometrics', 'rect', 'orange'),
        (3, 9.5, 'Fingerprint?\nCaptureFingerprint()\nFingerprintCNN.Extract()', 'rect', 'lightcyan'),
        (6, 9.5, 'Face?\nCaptureFaceImage()\nArcFace.Extract()', 'rect', 'lightcyan'),
        (9, 9.5, 'Palm?\nCapturePalmImage()\nPalmCNN.Extract()', 'rect', 'lightcyan'),
        (6, 8, 'userTemplates.size\n>= 2?', 'diamond', 'yellow'),
        (6, 6.5, 'Create user record:\n{Username, PasswordHash,\nBiometric Templates}', 'rect', 'lightblue'),
        (6, 5, 'UserDatabase.insert\n(record)', 'rect', 'lightblue'),
        (6, 3.5, 'Return Success\n"User registered"', 'rect', 'lightgreen'),
        (6, 2, 'END', 'ellipse', 'lightgreen'),
        (10, 18.5, 'Return Error\n"Username exists"', 'rect', 'red'),
        (10, 15.5, 'Return Error\n"Hello verification failed"', 'rect', 'red'),
        (10, 8, 'Return Error\n"Need >= 2 biometrics"', 'rect', 'red')
    ]
    
    for x, y, text, shape, color in reg_steps:
        if shape == 'ellipse':
            patch = Ellipse((x, y), 2.5, 0.8, facecolor=color, edgecolor='black', linewidth=2)
        elif shape == 'diamond':
            # Create diamond shape
            diamond = np.array([[x, y+0.6], [x+1.2, y], [x, y-0.6], [x-1.2, y]])
            patch = plt.Polygon(diamond, facecolor=color, edgecolor='black', linewidth=2)
        else:  # rectangle
            patch = FancyBboxPatch((x-1.5, y-0.5), 3, 1, boxstyle="round,pad=0.05",
                                  facecolor=color, edgecolor='black', linewidth=2)
        ax1.add_patch(patch)
        ax1.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Arrows for registration algorithm
    reg_arrows = [
        ((6, 22.6), (6, 21.9)),    # START to input
        ((6, 21.1), (6, 20.4)),    # input to check
        ((6, 19.6), (6, 19.1)),    # check to decision
        ((6, 18), (6, 17.4)),      # decision to hello (No)
        ((6, 16.6), (6, 16.1)),    # hello to decision
        ((6, 15), (6, 14.4)),      # decision to hash (Yes)
        ((6, 13.6), (6, 13)),      # hash to init
        ((6, 12.1), (6, 11.4)),    # init to loop
        ((6, 10.6), (3, 10)),      # loop to fingerprint
        ((6, 10.6), (6, 10)),      # loop to face
        ((6, 10.6), (9, 10)),      # loop to palm
        ((3, 9), (6, 8.5)),        # fingerprint to check
        ((6, 9), (6, 8.5)),        # face to check
        ((9, 9), (6, 8.5)),        # palm to check
        ((6, 7.4), (6, 6.9)),      # check to create (Yes)
        ((6, 6.1), (6, 5.4)),      # create to insert
        ((6, 4.6), (6, 3.9)),      # insert to success
        ((6, 3.1), (6, 2.4)),      # success to END
        
        # Error paths
        ((7.2, 18.5), (10, 18.5)), # username exists
        ((7.2, 15.5), (10, 15.5)), # hello failed
        ((7.2, 8), (10, 8))        # not enough biometrics
    ]
    
    for (x1, y1), (x2, y2) in reg_arrows:
        ax1.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    
    # Add decision labels for registration
    ax1.text(6.8, 17.5, 'No', ha='center', va='center', fontsize=10, color='green', fontweight='bold')
    ax1.text(7.2, 18.8, 'Yes', ha='center', va='center', fontsize=10, color='red', fontweight='bold')
    ax1.text(6.8, 14.5, 'Yes', ha='center', va='center', fontsize=10, color='green', fontweight='bold')
    ax1.text(7.2, 15.8, 'No', ha='center', va='center', fontsize=10, color='red', fontweight='bold')
    ax1.text(6.8, 7.5, 'Yes', ha='center', va='center', fontsize=10, color='green', fontweight='bold')
    ax1.text(7.2, 8.3, 'No', ha='center', va='center', fontsize=10, color='red', fontweight='bold')
    
    # Authentication Algorithm Flowchart
    ax2.set_xlim(0, 12)
    ax2.set_ylim(0, 24)
    ax2.axis('off')
    ax2.set_title('Authentication Algorithm (AuthenticateUser)', fontsize=18, fontweight='bold', pad=20)
    
    # Flowchart elements for authentication
    auth_steps = [
        (6, 23, 'START', 'ellipse', 'lightgreen'),
        (6, 21.5, 'Input: username, password\nchosenBiometric', 'rect', 'lightblue'),
        (6, 20, 'record = UserDatabase\n.find(username)', 'rect', 'lightblue'),
        (6, 18.5, 'User\nFound?', 'diamond', 'yellow'),
        (6, 17, 'VerifyHash(password,\nrecord.PasswordHash)', 'rect', 'lightblue'),
        (6, 15.5, 'Password\nCorrect?', 'diamond', 'yellow'),
        (6, 14, 'Check if chosen biometric\nexists for user', 'rect', 'lightblue'),
        (6, 12.5, 'Biometric\nAvailable?', 'diamond', 'yellow'),
        (6, 11, 'Capture live biometric\nsample', 'rect', 'orange'),
        (3, 9.5, 'Fingerprint:\nCaptureFingerprint()\nExtractFeatures()', 'rect', 'lightcyan'),
        (6, 9.5, 'Face:\nCaptureFaceImage()\nArcFaceExtract()', 'rect', 'lightcyan'),
        (9, 9.5, 'Palm:\nCapturePalmImage()\nExtractFeatures()', 'rect', 'lightcyan'),
        (6, 8, 'match_score =\nCompareTemplates()', 'rect', 'orange'),
        (6, 6.5, 'match_score >=\nMATCH_THRESHOLD?', 'diamond', 'yellow'),
        (6, 5, 'Generate session/token\nGrant access', 'rect', 'lightgreen'),
        (6, 3.5, 'Return Success\n"Authentication successful"', 'rect', 'lightgreen'),
        (6, 2, 'END', 'ellipse', 'lightgreen'),
        (10, 18.5, 'Return Failure\n"User not found"', 'rect', 'red'),
        (10, 15.5, 'Return Failure\n"Incorrect password"', 'rect', 'red'),
        (10, 12.5, 'Return Failure\n"Biometric not enrolled"', 'rect', 'red'),
        (10, 6.5, 'Return Failure\n"Biometric mismatch"', 'rect', 'red')
    ]
    
    for x, y, text, shape, color in auth_steps:
        if shape == 'ellipse':
            patch = Ellipse((x, y), 2.5, 0.8, facecolor=color, edgecolor='black', linewidth=2)
        elif shape == 'diamond':
            diamond = np.array([[x, y+0.6], [x+1.2, y], [x, y-0.6], [x-1.2, y]])
            patch = plt.Polygon(diamond, facecolor=color, edgecolor='black', linewidth=2)
        else:
            patch = FancyBboxPatch((x-1.5, y-0.5), 3, 1, boxstyle="round,pad=0.05",
                                  facecolor=color, edgecolor='black', linewidth=2)
        ax2.add_patch(patch)
        ax2.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Arrows for authentication algorithm
    auth_arrows = [
        ((6, 22.6), (6, 21.9)),     # START to input
        ((6, 21.1), (6, 20.4)),     # input to find
        ((6, 19.6), (6, 19.1)),     # find to decision
        ((6, 18), (6, 17.4)),       # decision to verify (Yes)
        ((6, 16.6), (6, 16.1)),     # verify to decision
        ((6, 15), (6, 14.4)),       # decision to check (Yes)
        ((6, 13.6), (6, 13.1)),     # check to decision
        ((6, 12), (6, 11.4)),       # decision to capture (Yes)
        ((6, 10.6), (3, 10)),       # capture to fingerprint
        ((6, 10.6), (6, 10)),       # capture to face
        ((6, 10.6), (9, 10)),       # capture to palm
        ((3, 9), (6, 8.5)),         # fingerprint to compare
        ((6, 9), (6, 8.5)),         # face to compare
        ((9, 9), (6, 8.5)),         # palm to compare
        ((6, 7.6), (6, 7.1)),       # compare to decision
        ((6, 6), (6, 5.4)),         # decision to grant (Yes)
        ((6, 4.6), (6, 3.9)),       # grant to success
        ((6, 3.1), (6, 2.4)),       # success to END
        
        # Error paths
        ((7.2, 18.5), (10, 18.5)),  # user not found
        ((7.2, 15.5), (10, 15.5)),  # wrong password
        ((7.2, 12.5), (10, 12.5)),  # biometric not available
        ((7.2, 6.5), (10, 6.5))     # biometric mismatch
    ]
    
    for (x1, y1), (x2, y2) in auth_arrows:
        ax2.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    
    # Add decision labels for authentication
    ax2.text(6.8, 17.5, 'Yes', ha='center', va='center', fontsize=10, color='green', fontweight='bold')
    ax2.text(7.2, 18.8, 'No', ha='center', va='center', fontsize=10, color='red', fontweight='bold')
    ax2.text(6.8, 14.5, 'Yes', ha='center', va='center', fontsize=10, color='green', fontweight='bold')
    ax2.text(7.2, 15.8, 'No', ha='center', va='center', fontsize=10, color='red', fontweight='bold')
    ax2.text(6.8, 11.5, 'Yes', ha='center', va='center', fontsize=10, color='green', fontweight='bold')
    ax2.text(7.2, 12.8, 'No', ha='center', va='center', fontsize=10, color='red', fontweight='bold')
    ax2.text(6.8, 5.5, 'Yes', ha='center', va='center', fontsize=10, color='green', fontweight='bold')
    ax2.text(7.2, 6.8, 'No', ha='center', va='center', fontsize=10, color='red', fontweight='bold')
    
    # Add algorithm details annotations
    ax1.text(1, 1, 'Key Features:\n• Multi-biometric enrollment\n• Windows Hello verification\n• Secure password hashing\n• Quality checks for captures\n• At least 2 biometrics required', 
            ha='left', va='bottom', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.9))
    
    ax2.text(1, 1, 'Key Features:\n• Two-factor authentication\n• Password verification first\n• Biometric matching second\n• Configurable thresholds\n• Detailed error handling', 
            ha='left', va='bottom', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig('diagrams/algorithm_design_diagrams.png', bbox_inches='tight', dpi=600)
    plt.close()
    print("✓ Algorithm Design Diagrams generated: diagrams/algorithm_design_diagrams.png")

def create_class_diagrams():
    """Generate Class Diagrams for the Biometric Authentication System"""
    fig, ax = plt.subplots(1, 1, figsize=(32, 24))
    ax.set_xlim(0, 36)
    ax.set_ylim(0, 28)
    ax.axis('off')
    
    # Title
    ax.text(18, 27.5, 'Biometric Authentication System - Class Diagram (C# WinUI Implementation)', 
            ha='center', va='center', fontsize=20, fontweight='bold')
    
    # Define classes with their attributes and methods
    classes = [
        {
            'name': 'User',
            'x': 6, 'y': 24, 'width': 5, 'height': 3.5,
            'attributes': [
                '- string username',
                '- string email', 
                '- string passwordHash',
                '- DateTime createdAt',
                '- bool isActive',
                '- List<BiometricTemplate> templates'
            ],
            'methods': [
                '+ bool CreateUser()',
                '+ bool ValidateCredentials()',
                '+ void UpdateProfile()',
                '+ void Deactivate()'
            ]
        },
        {
            'name': 'BiometricTemplate',
            'x': 15, 'y': 24, 'width': 5.5, 'height': 4,
            'attributes': [
                '- int id',
                '- string userId',
                '- BiometricType templateType',
                '- byte[] featureVector',
                '- DateTime createdAt',
                '- float qualityScore',
                '- bool isEncrypted'
            ],
            'methods': [
                '+ bool StoreTemplate()',
                '+ byte[] GetTemplate()',
                '+ float CompareTemplates()',
                '+ void DeleteTemplate()',
                '+ bool EncryptTemplate()'
            ]
        },
        {
            'name': 'RegistrationInterface',
            'x': 26, 'y': 24, 'width': 5, 'height': 3.5,
            'attributes': [
                '- Grid mainGrid',
                '- TextBox usernameBox',
                '- PasswordBox passwordBox',
                '- CheckBox[] modalitySelectors',
                '- ProgressBar progressBar'
            ],
            'methods': [
                '+ void InitializeComponent()',
                '+ void OnRegisterClick()',
                '+ void ShowProgress()',
                '+ void DisplayError()'
            ]
        },
        {
            'name': 'BiometricCaptureService',
            'x': 6, 'y': 19, 'width': 6, 'height': 4,
            'attributes': [
                '- OpenCVService cvService',
                '- VideoCapture camera',
                '- FingerprintSensor sensor',
                '- bool isCapturing',
                '- CaptureSettings settings'
            ],
            'methods': [
                '+ Mat CaptureFaceImage()',
                '+ Mat CaptureFingerprint()',
                '+ Mat CapturePalmprint()',
                '+ bool CheckQuality(Mat image)',
                '+ Mat PreprocessImage(Mat image)'
            ]
        },
        {
            'name': 'ArcFaceModel',
            'x': 15, 'y': 19, 'width': 5.5, 'height': 4,
            'attributes': [
                '- InferenceSession session',
                '- string modelPath',
                '- int inputSize = 112',
                '- int embeddingSize = 512',
                '- bool isLoaded'
            ],
            'methods': [
                '+ bool LoadModel()',
                '+ float[] ExtractFeatures(Mat face)',
                '+ Mat DetectAndCropFace(Mat image)',
                '+ float CalculateSimilarity()',
                '+ void Dispose()'
            ]
        },
        {
            'name': 'FingerprintCNN',
            'x': 26, 'y': 19, 'width': 5, 'height': 4,
            'attributes': [
                '- InferenceSession session',
                '- string modelPath',
                '- int inputSize = 224',
                '- int featureSize = 256',
                '- PreprocessingPipeline pipeline'
            ],
            'methods': [
                '+ bool LoadModel()',
                '+ float[] ExtractFeatures(Mat finger)',
                '+ Mat EnhanceFingerprint(Mat image)',
                '+ float CompareFingerprints()',
                '+ void Dispose()'
            ]
        },
        {
            'name': 'WindowsHelloService',
            'x': 6, 'y': 14, 'width': 6, 'height': 3.5,
            'attributes': [
                '- UserConsentVerifier verifier',
                '- string requestMessage',
                '- bool isAvailable',
                '- HelloAuthenticationKind authKind'
            ],
            'methods': [
                '+ bool IsHelloAvailable()',
                '+ Task<bool> VerifyUserPresence()',
                '+ bool CheckDeviceCapabilities()',
                '+ void DisplayPrompt(string message)'
            ]
        },
        {
            'name': 'AuthenticationService',
            'x': 15, 'y': 14, 'width': 5.5, 'height': 4,
            'attributes': [
                '- DatabaseManager dbManager',
                '- BiometricCaptureService captureService',
                '- SecurityManager security',
                '- float matchThreshold = 0.85f'
            ],
            'methods': [
                '+ bool AuthenticateUser()',
                '+ bool VerifyPassword()',
                '+ bool VerifyBiometric()',
                '+ Session CreateSession()',
                '+ void LogAttempt()'
            ]
        },
        {
            'name': 'PalmprintCNN',
            'x': 26, 'y': 14, 'width': 5, 'height': 3.5,
            'attributes': [
                '- InferenceSession session',
                '- string modelPath',
                '- int inputSize = 256',
                '- int featureSize = 512',
                '- RoiExtractor roiExtractor'
            ],
            'methods': [
                '+ bool LoadModel()',
                '+ float[] ExtractFeatures(Mat palm)',
                '+ Mat ExtractPalmROI(Mat image)',
                '+ float ComparePalms()',
                '+ void Dispose()'
            ]
        },
        {
            'name': 'DatabaseManager',
            'x': 6, 'y': 9, 'width': 5.5, 'height': 4,
            'attributes': [
                '- SQLiteConnection connection',
                '- string connectionString',
                '- EncryptionService encryption',
                '- bool isConnected'
            ],
            'methods': [
                '+ bool Initialize()',
                '+ bool InsertUser(User user)',
                '+ User FindUser(string username)',
                '+ bool UpdateUser(User user)',
                '+ bool BackupDatabase()',
                '+ void CloseConnection()'
            ]
        },
        {
            'name': 'SecurityManager',
            'x': 15, 'y': 9, 'width': 5, 'height': 4,
            'attributes': [
                '- string encryptionKey',
                '- HashAlgorithm hashAlgorithm',
                '- int saltLength = 16',
                '- int hashIterations = 10000'
            ],
            'methods': [
                '+ string HashPassword(string password)',
                '+ bool VerifyPassword()',
                '+ byte[] EncryptData(byte[] data)',
                '+ byte[] DecryptData(byte[] data)',
                '+ string GenerateSalt()'
            ]
        },
        {
            'name': 'LoginInterface',
            'x': 26, 'y': 9, 'width': 5, 'height': 3.5,
            'attributes': [
                '- Grid loginGrid',
                '- TextBox usernameBox',
                '- PasswordBox passwordBox',
                '- ComboBox modalitySelector',
                '- Button loginButton'
            ],
            'methods': [
                '+ void InitializeComponent()',
                '+ void OnLoginClick()',
                '+ void ShowBiometricPrompt()',
                '+ void NavigateToMain()'
            ]
        },
        {
            'name': 'ONNXRuntimeManager',
            'x': 6, 'y': 4, 'width': 6, 'height': 3.5,
            'attributes': [
                '- SessionOptions options',
                '- Dictionary<string, InferenceSession> sessions',
                '- bool useGPU',
                '- ExecutionProvider provider'
            ],
            'methods': [
                '+ InferenceSession LoadSession()',
                '+ float[] RunInference()',
                '+ void OptimizeSession()',
                '+ void DisposeAll()'
            ]
        },
        {
            'name': 'BiometricType',
            'x': 15, 'y': 4, 'width': 4, 'height': 2.5,
            'attributes': [
                'FINGERPRINT',
                'FACE', 
                'PALMPRINT'
            ],
            'methods': []
        },
        {
            'name': 'AdminInterface',
            'x': 26, 'y': 4, 'width': 5, 'height': 3.5,
            'attributes': [
                '- DataGrid userGrid',
                '- Chart analyticsChart',
                '- TextBlock statusText',
                '- Button[] adminButtons'
            ],
            'methods': [
                '+ void LoadUserData()',
                '+ void GenerateReports()',
                '+ void ResetUserCredentials()',
                '+ void ViewAuditLogs()'
            ]
        }
    ]
    
    # Draw classes
    for cls in classes:
        # Class rectangle
        rect = Rectangle((cls['x'] - cls['width']/2, cls['y'] - cls['height']/2), 
                        cls['width'], cls['height'], 
                        facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        
        # Class name (header)
        header_height = 0.6
        header_rect = Rectangle((cls['x'] - cls['width']/2, cls['y'] + cls['height']/2 - header_height), 
                               cls['width'], header_height, 
                               facecolor='darkblue', edgecolor='black', linewidth=1)
        ax.add_patch(header_rect)
        
        ax.text(cls['x'], cls['y'] + cls['height']/2 - header_height/2, cls['name'], 
               ha='center', va='center', fontsize=11, fontweight='bold', color='white')
        
        # Attributes section
        attr_start_y = cls['y'] + cls['height']/2 - header_height - 0.1
        attr_y = attr_start_y
        for attr in cls['attributes']:
            ax.text(cls['x'] - cls['width']/2 + 0.1, attr_y, attr, 
                   ha='left', va='top', fontsize=8)
            attr_y -= 0.25
        
        # Separator line (only if there are methods)
        if cls['methods']:
            separator_y = attr_y + 0.1
            ax.plot([cls['x'] - cls['width']/2, cls['x'] + cls['width']/2], 
                   [separator_y, separator_y], 'k-', linewidth=1)
            
            # Methods section
            method_y = separator_y - 0.1
            for method in cls['methods']:
                ax.text(cls['x'] - cls['width']/2 + 0.1, method_y, method, 
                       ha='left', va='top', fontsize=8)
                method_y -= 0.25
    
    # Define relationships
    relationships = [
        # (from_class, to_class, relationship_type, label)
        ('User', 'BiometricTemplate', 'one_to_many', '1..*'),
        ('RegistrationInterface', 'BiometricCaptureService', 'uses', 'captures'),
        ('RegistrationInterface', 'WindowsHelloService', 'uses', 'verifies'),
        ('BiometricCaptureService', 'ArcFaceModel', 'uses', 'processes face'),
        ('BiometricCaptureService', 'FingerprintCNN', 'uses', 'processes finger'),
        ('BiometricCaptureService', 'PalmprintCNN', 'uses', 'processes palm'),
        ('AuthenticationService', 'DatabaseManager', 'uses', 'queries'),
        ('AuthenticationService', 'SecurityManager', 'uses', 'verifies'),
        ('LoginInterface', 'AuthenticationService', 'uses', 'authenticates'),
        ('DatabaseManager', 'User', 'manages', 'stores'),
        ('DatabaseManager', 'BiometricTemplate', 'manages', 'stores'),
        ('ArcFaceModel', 'ONNXRuntimeManager', 'uses', 'inference'),
        ('FingerprintCNN', 'ONNXRuntimeManager', 'uses', 'inference'),
        ('PalmprintCNN', 'ONNXRuntimeManager', 'uses', 'inference'),
        ('BiometricTemplate', 'BiometricType', 'uses', 'type'),
        ('AdminInterface', 'DatabaseManager', 'uses', 'queries')
    ]
    
    # Class positions for relationship drawing
    class_positions = {cls['name']: (cls['x'], cls['y']) for cls in classes}
    
    # Draw relationships
    for from_cls, to_cls, rel_type, label in relationships:
        if from_cls in class_positions and to_cls in class_positions:
            x1, y1 = class_positions[from_cls]
            x2, y2 = class_positions[to_cls]
            
            # Calculate connection points (edges of rectangles)
            from_cls_obj = next(cls for cls in classes if cls['name'] == from_cls)
            to_cls_obj = next(cls for cls in classes if cls['name'] == to_cls)
            
            # Simple connection from center to center for now
            if abs(x1 - x2) > abs(y1 - y2):  # Horizontal connection
                if x1 < x2:
                    start_x = x1 + from_cls_obj['width']/2
                    end_x = x2 - to_cls_obj['width']/2
                else:
                    start_x = x1 - from_cls_obj['width']/2
                    end_x = x2 + to_cls_obj['width']/2
                start_y, end_y = y1, y2
            else:  # Vertical connection
                if y1 > y2:
                    start_y = y1 - from_cls_obj['height']/2
                    end_y = y2 + to_cls_obj['height']/2
                else:
                    start_y = y1 + from_cls_obj['height']/2
                    end_y = y2 - to_cls_obj['height']/2
                start_x, end_x = x1, x2
            
            # Draw arrow based on relationship type
            if rel_type == 'one_to_many':
                ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                           arrowprops=dict(arrowstyle='-|>', color='blue', lw=2))
            elif rel_type == 'uses':
                ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                           arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
            else:  # manages
                ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                           arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
            
            # Add relationship label
            mid_x, mid_y = (start_x + end_x) / 2, (start_y + end_y) / 2
            ax.text(mid_x, mid_y + 0.3, label, ha='center', va='bottom', 
                   fontsize=8, bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    # Add legend
    legend_elements = [
        ('Uses Relationship', 'green', '->'),
        ('One-to-Many', 'blue', '-|>'),
        ('Manages', 'red', '->')
    ]
    
    legend_y = 2.5
    ax.text(2, 3, 'Relationships:', ha='left', va='center', fontsize=12, fontweight='bold')
    for rel_name, color, arrow in legend_elements:
        ax.text(2, legend_y, f'{rel_name}:', ha='left', va='center', fontsize=10)
        ax.annotate('', xy=(7, legend_y), xytext=(5, legend_y),
                   arrowprops=dict(arrowstyle=arrow, color=color, lw=2))
        legend_y -= 0.4
    
    # Add technology stack info
    tech_info = """
Technology Stack:
• Language: C# (.NET)
• UI Framework: WinUI 3
• Computer Vision: OpenCVSharp
• AI/ML Runtime: ONNX Runtime
• Database: SQLite with encryption
• Security: Windows Hello API
• Face Model: ArcFace (ResNet100)
• Custom CNNs: Fingerprint & Palmprint
"""
    ax.text(32, 15, tech_info, ha='left', va='center', fontsize=10,
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig('diagrams/class_diagrams.png', bbox_inches='tight', dpi=600)
    plt.close()
    print("✓ Class Diagrams generated: diagrams/class_diagrams.png")

def create_sequence_diagram():
    """Generate Sequence Diagram for Authentication Process"""
    fig, ax = plt.subplots(1, 1, figsize=(28, 18))
    ax.set_xlim(0, 28)
    ax.set_ylim(0, 20)
    ax.axis('off')
    
    # Title
    ax.text(14, 19.5, 'Biometric Authentication - Sequence Diagram (C# WinUI)', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    # Actors/Objects
    actors = [
        (3, 18, 'Staff User'),
        (7, 18, 'Login Interface\n(WinUI)'),
        (11, 18, 'Authentication\nService'),
        (15, 18, 'Biometric Capture\nService'),
        (19, 18, 'ONNX Models\n(ArcFace/CNN)'),
        (23, 18, 'Database\nManager'),
        (27, 18, 'Windows Hello\nService')
    ]
    
    # Draw actors
    for x, y, name in actors:
        rect = Rectangle((x-1.2, y-0.5), 2.4, 1, facecolor='lightblue', 
                        edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, name, ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Lifeline
        ax.plot([x, x], [y-0.5, 1], 'k--', linewidth=1.5)
    
    # Authentication sequence messages
    messages = [
        # Initial login
        (3, 7, 'Enter username/password'),
        (7, 11, 'Authenticate(username, password)'),
        (11, 23, 'FindUser(username)'),
        (23, 11, 'User record'),
        (11, 11, 'VerifyPassword(password, hash)'),
        
        # Biometric selection and capture
        (7, 11, 'SelectBiometric(modality)'),
        (11, 15, 'CaptureBiometric(modality)'),
        (15, 15, 'StartCapture(camera/sensor)'),
        (15, 7, 'Display capture UI'),
        (3, 15, 'Provide biometric sample'),
        
        # Feature extraction
        (15, 19, 'ProcessImage(rawImage)'),
        (19, 15, 'ExtractFeatures(processedImage)'),
        (19, 15, 'Return feature vector'),
        
        # Template matching
        (15, 23, 'GetStoredTemplate(userID, modality)'),
        (23, 15, 'Biometric template'),
        (15, 15, 'CompareTemplates(live, stored)'),
        (15, 11, 'Match score'),
        
        # Decision and response
        (11, 11, 'Evaluate threshold'),
        (11, 7, 'Authentication result'),
        (7, 3, 'Show success/failure'),
        
        # Optional Windows Hello verification
        (11, 27, 'VerifyUserPresence()'),
        (27, 11, 'Windows Hello result')
    ]
    
    y_pos = 17
    for from_x, to_x, message in messages:
        y = y_pos - 0.5
        
        # Draw arrow
        if from_x < to_x:
            ax.annotate('', xy=(to_x-0.2, y), xytext=(from_x+0.2, y),
                       arrowprops=dict(arrowstyle='->', color='blue', lw=2))
        else:
            ax.annotate('', xy=(to_x+0.2, y), xytext=(from_x-0.2, y),
                       arrowprops=dict(arrowstyle='->', color='red', lw=2))
        
        # Add message label
        mid_x = (from_x + to_x) / 2
        ax.text(mid_x, y + 0.2, message, ha='center', va='bottom', fontsize=9,
               bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.9))
        y_pos -= 0.5
    
    # Add activation boxes
    activations = [
        (7, 16.5, 7),      # Login Interface
        (11, 15.5, 6.5),   # Authentication Service  
        (15, 13.5, 8.5),   # Biometric Capture
        (19, 11.5, 10.5),  # ONNX Models
        (23, 15.5, 9.5),   # Database
        (27, 6.5, 6)       # Windows Hello
    ]
    
    for x, start_y, end_y in activations:
        rect = Rectangle((x-0.15, end_y), 0.3, start_y-end_y, 
                        facecolor='yellow', edgecolor='black', linewidth=1)
        ax.add_patch(rect)
    
    # Add notes for key processes
    notes = [
        (5, 3, 'Two-Factor Authentication:\n1. Password verification\n2. Biometric matching'),
        (17, 3, 'AI/ML Processing:\n• ArcFace for face recognition\n• Custom CNNs for fingerprint/palm\n• ONNX Runtime execution'),
        (25, 3, 'Security Features:\n• Encrypted storage\n• Windows Hello integration\n• Audit logging')
    ]
    
    for x, y, note in notes:
        ax.text(x, y, note, ha='center', va='center', fontsize=9,
               bbox=dict(boxstyle="round,pad=0.4", facecolor='lightyellow', alpha=0.9))
    
    plt.tight_layout()
    plt.savefig('diagrams/sequence_diagram.png', bbox_inches='tight', dpi=600)
    plt.close()
    print("✓ Sequence Diagram generated: diagrams/sequence_diagram.png")

def create_entity_relationship_diagram():
    """Generate Entity Relationship Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(24, 16))
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 16)
    ax.axis('off')
    
    # Title
    ax.text(12, 15.5, 'Biometric Authentication System - Entity Relationship Diagram (SQLite)', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    # Entities
    entities = [
        {
            'name': 'Users',
            'x': 5, 'y': 12, 'width': 4, 'height': 3.5,
            'attributes': ['id (PK)', 'username (UNIQUE)', 'email', 'password_hash', 'created_at', 'is_active', 'last_login']
        },
        {
            'name': 'Biometric_Templates',
            'x': 12, 'y': 12, 'width': 4.5, 'height': 4,
            'attributes': ['id (PK)', 'user_id (FK)', 'template_type', 'feature_vector (BLOB)', 'created_at', 'quality_score', 'is_encrypted', 'algorithm_version']
        },
        {
            'name': 'Login_Attempts',
            'x': 19, 'y': 12, 'width': 4, 'height': 3.5,
            'attributes': ['id (PK)', 'user_id (FK)', 'attempt_time', 'success', 'biometric_used', 'match_score', 'failure_reason']
        },
        {
            'name': 'Registration_Sessions',
            'x': 5, 'y': 7, 'width': 4, 'height': 3,
            'attributes': ['id (PK)', 'user_id (FK)', 'session_start', 'session_end', 'windows_hello_verified', 'status']
        },
        {
            'name': 'Audit_Logs',
            'x': 12, 'y': 7, 'width': 4.5, 'height': 3,
            'attributes': ['id (PK)', 'user_id (FK)', 'action_type', 'timestamp', 'details (JSON)', 'ip_address']
        },
        {
            'name': 'System_Configuration',
            'x': 19, 'y': 7, 'width': 4, 'height': 2.5,
            'attributes': ['id (PK)', 'config_key', 'config_value', 'updated_at', 'updated_by']
        },
        {
            'name': 'Template_Backups',
            'x': 5, 'y': 3, 'width': 4, 'height': 2.5,
            'attributes': ['id (PK)', 'template_id (FK)', 'backup_date', 'encrypted_data', 'checksum']
        },
        {
            'name': 'Performance_Metrics',
            'x': 12, 'y': 3, 'width': 4.5, 'height': 2.5,
            'attributes': ['id (PK)', 'metric_type', 'value', 'timestamp', 'context_data']
        }
    ]
    
    # Draw entities
    for entity in entities:
        # Entity rectangle
        rect = Rectangle((entity['x'] - entity['width']/2, entity['y'] - entity['height']/2), 
                        entity['width'], entity['height'], 
                        facecolor='lightcyan', edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        
        # Entity name
        ax.text(entity['x'], entity['y'] + entity['height']/2 - 0.3, entity['name'], 
               ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Attributes
        attr_y = entity['y'] + entity['height']/2 - 0.7
        for attr in entity['attributes']:
            ax.text(entity['x'] - entity['width']/2 + 0.1, attr_y, attr, 
                   ha='left', va='center', fontsize=9)
            attr_y -= 0.3
    
    # Relationships
    relationships = [
        # (entity1, entity2, relationship, cardinality1, cardinality2, label)
        ('Users', 'Biometric_Templates', 'has', '1', 'M', 'enrolls'),
        ('Users', 'Login_Attempts', 'generates', '1', 'M', 'attempts'),
        ('Users', 'Registration_Sessions', 'initiates', '1', 'M', 'registers'),
        ('Users', 'Audit_Logs', 'creates', '1', 'M', 'actions'),
        ('Biometric_Templates', 'Template_Backups', 'backed_up_to', '1', 'M', 'backup'),
    ]
    
    # Entity positions
    entity_pos = {entity['name']: (entity['x'], entity['y']) for entity in entities}
    
    # Draw relationships
    for ent1, ent2, rel_name, card1, card2, label in relationships:
        if ent1 in entity_pos and ent2 in entity_pos:
            x1, y1 = entity_pos[ent1]
            x2, y2 = entity_pos[ent2]
            
            # Calculate connection points
            if abs(x1 - x2) > abs(y1 - y2):  # Horizontal connection
                if x1 < x2:
                    conn_x1, conn_x2 = x1 + 2, x2 - 2.25
                else:
                    conn_x1, conn_x2 = x1 - 2, x2 + 2.25
                conn_y1, conn_y2 = y1, y2
            else:  # Vertical connection
                if y1 > y2:
                    conn_y1, conn_y2 = y1 - 1.75, y2 + 1.5
                else:
                    conn_y1, conn_y2 = y1 + 1.75, y2 - 1.5
                conn_x1, conn_x2 = x1, x2
            
            # Draw relationship line
            ax.plot([conn_x1, conn_x2], [conn_y1, conn_y2], 'k-', linewidth=2)
            
            # Add relationship diamond
            mid_x, mid_y = (conn_x1 + conn_x2) / 2, (conn_y1 + conn_y2) / 2
            diamond = np.array([[mid_x, mid_y+0.4], [mid_x+0.6, mid_y], 
                               [mid_x, mid_y-0.4], [mid_x-0.6, mid_y]])
            diamond_patch = plt.Polygon(diamond, facecolor='yellow', edgecolor='black', linewidth=2)
            ax.add_patch(diamond_patch)
            
            ax.text(mid_x, mid_y, label, ha='center', va='center', fontsize=9, fontweight='bold')
            
            # Add cardinalities
            offset = 0.3
            ax.text(conn_x1 + (offset if conn_x1 < conn_x2 else -offset), 
                   conn_y1 + (offset if conn_y1 < conn_y2 else -offset), 
                   card1, ha='center', va='center', 
                   fontsize=11, fontweight='bold', color='red')
            ax.text(conn_x2 + (-offset if conn_x1 < conn_x2 else offset), 
                   conn_y2 + (-offset if conn_y1 < conn_y2 else offset), 
                   card2, ha='center', va='center', 
                   fontsize=11, fontweight='bold', color='red')
    
    # Add database schema notes
    schema_notes = [
        (2, 1.5, 'Database: SQLite\nEncryption: AES-256\nIndices: username, user_id, timestamp'),
        (12, 1, 'Key Features:\n• BLOB storage for feature vectors\n• JSON fields for flexible data\n• Foreign key constraints\n• Automatic timestamps'),
        (21, 1.5, 'Performance:\n• Indexed lookups\n• Batch operations\n• Connection pooling\n• Query optimization')
    ]
    
    for x, y, note in schema_notes:
        ax.text(x, y, note, ha='center', va='center', fontsize=10,
               bbox=dict(boxstyle="round,pad=0.4", facecolor='lightyellow', alpha=0.9))
    
    # Add legend
    ax.text(1, 14, 'Legend:', ha='left', va='center', fontsize=12, fontweight='bold')
    ax.text(1, 13.5, 'PK = Primary Key', ha='left', va='center', fontsize=10)
    ax.text(1, 13.2, 'FK = Foreign Key', ha='left', va='center', fontsize=10)
    ax.text(1, 12.9, '1 = One, M = Many', ha='left', va='center', fontsize=10)
    ax.text(1, 12.6, 'BLOB = Binary Large Object', ha='left', va='center', fontsize=10)
    ax.text(1, 12.3, 'JSON = JavaScript Object Notation', ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('diagrams/entity_relationship_diagram.png', bbox_inches='tight', dpi=600)
    plt.close()
    print("✓ Entity Relationship Diagram generated: diagrams/entity_relationship_diagram.png")

def main():
    """Generate all diagrams"""
    print("🎨 Generating Comprehensive Diagrams for Biometric Authentication System...")
    print("=" * 70)
    
    # Create all diagrams
    create_use_case_diagram()
    create_data_flow_diagram()
    create_system_architecture_diagram()
    create_algorithm_design_diagrams()
    create_class_diagrams()
    create_sequence_diagram()
    create_entity_relationship_diagram()
    
    print("=" * 70)
    print("✅ All diagrams generated successfully!")
    print(f"📁 Check the 'diagrams' folder for all generated files:")
    print("   • use_case_diagram.png")
    print("   • data_flow_diagram.png")
    print("   • system_architecture_diagram.png")
    print("   • algorithm_design_diagrams.png")
    print("   • class_diagrams.png")
    print("   • sequence_diagram.png")
    print("   • entity_relationship_diagram.png")
    print(f"\n🕐 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
