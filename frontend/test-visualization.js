// Test script to understand current dashboard data structure
// Run this in browser console on the dashboard page

console.log('Testing visualization modal...');

// Mock biometric entry with analysis data for testing
const mockEntry = {
  id: 1,
  type: 'face',
  has_analysis: true,
  analysis_data: {
    generated_visualizations: [
      {
        id: 'viz1',
        type: 'feature_extraction',
        title: 'Facial Feature Points',
        description: 'Key facial landmarks detected during analysis',
        data: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
        format: 'image/png'
      },
      {
        id: 'viz2',
        type: 'quality_analysis',
        title: 'Quality Metrics Visualization',
        description: 'Visual representation of biometric quality scores',
        data: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
        format: 'image/png'
      }
    ],
    processing_steps: [
      'Image preprocessing',
      'Feature extraction', 
      'Quality assessment',
      'Template generation',
      'Matching analysis'
    ],
    quality_score: 87.5,
    processing_time: '2.34s'
  }
};

// Test if VisualizationModal can be accessed
if (window.React) {
  console.log('React is available');
  console.log('Mock entry for testing:', mockEntry);
  
  // Instructions for manual testing
  console.log(`
To test the visualization modal:
1. Open browser dev tools
2. Go to Components tab (React Developer Tools)
3. Find BiometricAnalysisDashboard component
4. Look for the eye icon buttons in the Personal Analytics table
5. Click an eye icon to test the modal functionality

Mock data structure expected:
- entry.id: unique identifier
- entry.type: biometric type (face, fingerprint, voice)
- entry.has_analysis: boolean indicating if analysis data exists
- entry.analysis_data.generated_visualizations: array of visualization objects
- Each visualization should have: id, type, title, description, data (base64), format
  `);
} else {
  console.log('React not found - make sure you are on the dashboard page');
}
