/**
 * 显示所有服务的访问地址
 */

// 定义服务地址
const services = {
  frontend: {
    name: '前端应用 (Frontend)',
    url: 'http://localhost:3000',
    description: 'Next.js 应用，提供用户界面'
  },
  backend: {
    name: '后端服务 (Backend)',
    url: 'http://localhost:8000',
    description: 'FastAPI 服务，提供 API 接口'
  },
  docs: {
    name: '项目文档 (Documentation)',
    url: 'http://localhost:5173',
    description: 'VitePress 文档站点'
  },
  apiDocs: [
    {
      name: 'API 文档 - Swagger UI',
      url: 'http://localhost:8000/api/docs',
      description: '交互式 API 文档'
    },
    {
      name: 'API 文档 - ReDoc',
      url: 'http://localhost:8000/api/redoc',
      description: '可读性更好的 API 文档'
    }
  ]
};

// 创建分隔线
const separator = '='.repeat(60);

// 输出标题
console.log('\n' + separator);
console.log('🚀 AIDA 项目服务地址');
console.log(separator + '\n');

// 输出主要服务
console.log('📱 主要服务:');
Object.values(services).forEach(service => {
  if (!Array.isArray(service)) {
    console.log(`• ${service.name}: ${service.url}`);
    console.log(`  ${service.description}\n`);
  }
});

// 输出 API 文档
console.log('📚 API 文档:');
services.apiDocs.forEach(doc => {
  console.log(`• ${doc.name}: ${doc.url}`);
  console.log(`  ${doc.description}\n`);
});

// 提示信息
console.log('提示: 按 Ctrl+C 可以停止所有服务\n');

// 保持脚本运行，直到用户按 Ctrl+C
console.log('服务地址信息将保持显示，直到项目停止运行...'); 