const fs = require('fs');
const path = require('path');

// Replace environment variables in built files at runtime
function replaceEnvInBuiltFiles() {
  const buildDir = path.join(__dirname, 'build', 'static', 'js');
  const apiUrl = process.env.REACT_APP_API_URL || 'https://backend-production-9ec1.up.railway.app/api/v1';
  
  console.log(`Replacing localhost references with: ${apiUrl}`);
  
  if (!fs.existsSync(buildDir)) {
    console.log('Build directory not found, skipping environment replacement');
    return;
  }
  
  const jsFiles = fs.readdirSync(buildDir).filter(file => file.endsWith('.js'));
  
  jsFiles.forEach(file => {
    const filePath = path.join(buildDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Replace all localhost references with the production URL
    const originalLength = content.length;
    content = content.replace(/http:\/\/localhost:8000\/api\/v1/g, apiUrl);
    content = content.replace(/localhost:8000/g, apiUrl.replace('https://', '').replace('/api/v1', ''));
    
    if (content.length !== originalLength) {
      fs.writeFileSync(filePath, content);
      console.log(`Updated ${file}: replaced localhost references`);
    } else {
      console.log(`No localhost references found in ${file}`);
    }
  });
}

replaceEnvInBuiltFiles();
