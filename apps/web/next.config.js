/** @type {import('next').NextConfig} */

const nextConfig = {

  reactStrictMode: true,

  poweredByHeader: false,

  experimental: {

    optimizePackageImports: [
      "react-icons"
    ]
  },

  images: {

    remotePatterns: [

      {
        protocol: "https",

        hostname: "**"
      }
    ]
  }
}

module.exports = nextConfig