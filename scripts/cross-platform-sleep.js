/**
 * 跨平台延迟脚本
 * 在 Windows、macOS 和 Linux 上提供统一的延迟功能
 * 使用方法: node cross-platform-sleep.js <seconds>
 */

// 获取延迟秒数
const seconds = process.argv[2] || 3;

console.log(`Waiting for ${seconds} seconds...`);

// 使用 setTimeout 实现延迟
setTimeout(() => {
  console.log('Done waiting.');
  process.exit(0);
}, seconds * 1000); 