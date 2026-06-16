/** @type {import('next').NextConfig} */
// import { fileURLToPath } from "url";
// import path from "path";

// const filename = fileURLToPath(import.meta.url);
// const dirname = path.dirname(filename);

const nextConfig = {
  // turbopack: {
  //   // Points Turbopack strictly to your actual Next.js application directory
  //   root: dirname,
  // },
  /* config options here */
  reactCompiler: true,
  // outputFileTracingRoot: path.join(dirname),
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "finguard-media.s3.us-east-1.amazonaws.com",
        port: "",
        pathname: "/**",
      },
    ],
  },
};

export default nextConfig;
