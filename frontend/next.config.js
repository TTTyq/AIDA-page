/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // 添加图片域名配置
  images: {
    domains: ['picsum.photos', 'images.unsplash.com'],
  },
};

module.exports = nextConfig;
