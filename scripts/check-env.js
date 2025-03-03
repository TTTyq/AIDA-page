const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Define paths
const backendDir = path.join(__dirname, '..', 'backend');
const envPath = path.join(backendDir, '.env');
const envExamplePath = path.join(backendDir, '.env.example');

// Check if .env file exists in backend directory
if (!fs.existsSync(envPath)) {
  console.log('\x1b[33m%s\x1b[0m', 'Warning: .env file not found in backend directory.');
  
  // Check if .env.example exists
  if (fs.existsSync(envExamplePath)) {
    console.log('\x1b[36m%s\x1b[0m', 'Creating .env file from .env.example...');
    
    try {
      // Copy .env.example to .env
      fs.copyFileSync(envExamplePath, envPath);
      console.log('\x1b[32m%s\x1b[0m', 'Successfully created .env file from .env.example.');
      console.log('\x1b[33m%s\x1b[0m', 'Please review and update the values in the .env file if needed.');
    } catch (error) {
      console.error('\x1b[31m%s\x1b[0m', `Error creating .env file: ${error.message}`);
      console.log('\x1b[36m%s\x1b[0m', 'Please manually copy .env.example to .env with the following command:');
      console.log(`cp ${envExamplePath} ${envPath}`);
      process.exit(1);
    }
  } else {
    console.error('\x1b[31m%s\x1b[0m', 'Error: Neither .env nor .env.example files found in backend directory.');
    console.log('\x1b[36m%s\x1b[0m', 'Please create a .env file with the required environment variables.');
    process.exit(1);
  }
} else {
  console.log('\x1b[32m%s\x1b[0m', '.env file found in backend directory.');
}

// Check if MongoDB is running
try {
  console.log('Checking if MongoDB is running...');
  
  // Different commands based on platform
  if (process.platform === 'win32') {
    // Windows
    try {
      const output = execSync('sc query MongoDB').toString();
      if (output.includes('RUNNING')) {
        console.log('\x1b[32m%s\x1b[0m', 'MongoDB is running.');
      } else {
        throw new Error('MongoDB service is not running');
      }
    } catch (error) {
      console.error('\x1b[31m%s\x1b[0m', 'Error: MongoDB is not running.');
      console.log('\x1b[36m%s\x1b[0m', 'Please start MongoDB using one of these methods:');
      console.log('1. Open Services (services.msc) and start MongoDB');
      console.log('2. Run command: net start MongoDB');
      process.exit(1);
    }
  } else {
    // macOS/Linux
    try {
      execSync('pgrep -x mongod || pgrep -x mongodb');
      console.log('\x1b[32m%s\x1b[0m', 'MongoDB is running.');
    } catch (error) {
      console.error('\x1b[31m%s\x1b[0m', 'Error: MongoDB is not running.');
      console.log('\x1b[36m%s\x1b[0m', 'Please start MongoDB with one of the following commands:');
      console.log('- brew services start mongodb-community (macOS with Homebrew)');
      console.log('- sudo systemctl start mongod (Linux with systemd)');
      console.log('- mongod (direct command)');
      process.exit(1);
    }
  }
} catch (error) {
  console.error('\x1b[31m%s\x1b[0m', `Error checking MongoDB status: ${error.message}`);
}

console.log('\x1b[32m%s\x1b[0m', 'Environment check completed successfully.'); 