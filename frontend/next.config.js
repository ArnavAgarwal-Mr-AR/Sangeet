/** @type {import('next').NextConfig} */
const nextConfig = {
    webpack(config) {
      // config.cache = false; // Disable caching
      config.module.rules.push({
        test: /\.html$/,
        use: 'raw-loader',
      })
      // config.infrastructureLogging = { debug: /PackFileCache/ }
      return config;
    },
    experimental: {
      serverActions: {
        bodySizeLimit: '10mb',
      },
    },
    typescript: {
      ignoreBuildErrors: true,
    },
    eslint: {
      ignoreDuringBuilds: true,
    },
    images: {
      remotePatterns: [
        {
          protocol: 'https',
          hostname: '**',
        },
        {
          protocol: 'http',
          hostname: '*',
        },
      ],
    },
  }
  
  module.exports = nextConfig