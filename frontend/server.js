// Express server to serve React build
const express = require('express');
const path = require('path');
const app = express();

const BUILD_DIR = path.join(__dirname, 'build');
app.use(express.static(BUILD_DIR));

// All remaining requests return the React app
app.get('*', function(req, res) {
  res.sendFile(path.join(BUILD_DIR, 'index.html'));
});

// Start the server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Frontend server listening on port ${PORT}`);
});
