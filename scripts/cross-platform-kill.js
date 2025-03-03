/**
 * 跨平台进程终止脚本
 * 在 Windows、macOS 和 Linux 上提供统一的进程终止功能
 */

const { execSync } = require('child_process');

// 要终止的进程名称或模式
const processPattern = 'uvicorn main:app';

try {
  console.log(`Attempting to terminate process matching: ${processPattern}`);
  
  if (process.platform === 'win32') {
    // Windows - 使用 taskkill
    try {
      execSync(`taskkill /F /FI "WINDOWTITLE eq ${processPattern}"`, { stdio: 'ignore' });
      execSync(`taskkill /F /FI "IMAGENAME eq python.exe" /FI "COMMANDLINE eq *${processPattern}*"`, { stdio: 'ignore' });
      console.log('Process terminated successfully on Windows.');
    } catch (error) {
      console.log('No matching process found or unable to terminate on Windows.');
    }
  } else {
    // macOS/Linux - 使用 pkill
    try {
      execSync(`pkill -f '${processPattern}'`, { stdio: 'ignore' });
      console.log('Process terminated successfully on macOS/Linux.');
    } catch (error) {
      console.log('No matching process found or unable to terminate on macOS/Linux.');
    }
  }
} catch (error) {
  console.error(`Error terminating process: ${error.message}`);
}

console.log('Process termination script completed.'); 