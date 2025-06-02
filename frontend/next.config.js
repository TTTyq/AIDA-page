const withLess = require('next-with-less');

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // 添加图片域名配置
  images: {
    domains: ['picsum.photos', 'images.unsplash.com'],
  },
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
  ...nextConfig,
}); 