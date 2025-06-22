This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, ensure you have [Node.js 22 LTS](https://nodejs.org) installed on your system.

Then, install the project dependencies:

```bash
npm install
```

After that, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Running Storybook

Storybook is a tool for developing UI components in isolation. It allows you to visualize and test components independently from the main application.

To run Storybook locally, use the following command:

```bash
npm run storybook
```

This will start the Storybook server on [http://localhost:6006](http://localhost:6006). Open this URL in your browser to explore the available components.

Storybook provides an interactive interface where you can view, test, and document your components. It supports addons like accessibility checks, documentation generation, and more.

To build a static version of Storybook for deployment, use:

```bash
npm run build-storybook
```

The static files will be generated in the `storybook-static` directory.

## Learn More

To learn more about Next.js and Storybook, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.
- [Storybook Documentation](https://storybook.js.org/docs) - learn about Storybook features and API.
- [Storybook GitHub Repository](https://github.com/storybookjs/storybook) - contribute and explore Storybook's development.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
