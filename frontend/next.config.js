const withLess = require('next-with-less');

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // 移除 standalone 输出配置，Vercel 不需要
  // output: 'standalone',
  // 添加图片域名配置
  images: {
    domains: ['picsum.photos', 'images.unsplash.com'],
  },
  // 移除本地 API 代理配置，Vercel 部署时不需要
  // async rewrites() {
  //   return [
  //     {
  //       source: '/api/:path*',
  //       destination: 'http://localhost:8000/api/v1/:path*',
  //     },
  //   ];
  // },
};

module.exports = withLess({
  lessLoaderOptions: {
    lessOptions: {
      javascriptEnabled: true,
      modifyVars: {
        '@primary-color': '#1976d2',
        '@secondary-color': '#9c27b0',
      },
    },
  },
  webpack(config) {
    // 添加CSS文件处理
    const rules = config.module.rules;
    
    // 查找并修改现有的CSS规则
    const cssRule = rules.find(
      (rule) => rule.test && rule.test.toString().includes('css')
    );
    
    if (cssRule) {
      // 确保CSS规则包含所有必要的加载器
      const cssLoaders = cssRule.use || cssRule.loader;
      if (cssLoaders && Array.isArray(cssLoaders)) {
        // 确保已经有必要的加载器
      } else {
        // 如果没有找到加载器，添加默认的CSS加载器
        cssRule.use = ['style-loader', 'css-loader', 'postcss-loader'];
      }
    } else {
      // 如果没有找到CSS规则，添加一个新规则
      rules.push({
        test: /\.css$/,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      });
    }
    
    // 添加Less文件处理
    rules.push({
      test: /\.less$/,
      use: [
        'style-loader',
        'css-loader',
        {
          loader: 'less-loader',
          options: {
            lessOptions: {
              javascriptEnabled: true,
            },
          },
        },
      ],
    });
    
    return config;
  },
  ...nextConfig,
}); 