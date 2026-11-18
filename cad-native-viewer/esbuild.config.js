const esbuild = require('esbuild');

const isProduction = process.argv.includes('--production');
const isWatch = process.argv.includes('--watch');

const emptyNodeModulesPlugin = {
  name: 'empty-node-modules',
  setup(build) {
    build.onResolve({ filter: /^(fs|path)$/ }, (args) => ({
      path: args.path,
      namespace: 'empty-node-modules',
    }));
    build.onLoad({ filter: /.*/, namespace: 'empty-node-modules' }, () => ({
      contents: 'module.exports = {};',
      loader: 'js',
    }));
  },
};

async function build() {
  console.log(`[build] Starting build (production: ${isProduction}, watch: ${isWatch})...`);

  // 1. Build Extension Host Bundle
  const extensionCtx = await esbuild.context({
    entryPoints: ['src/extension.ts'],
    bundle: true,
    format: 'cjs',
    minify: isProduction,
    sourcemap: !isProduction,
    sourcesContent: false,
    platform: 'node',
    outfile: 'dist/extension.js',
    external: ['vscode'],
    logLevel: 'info',
  });

  // 2. Build Webview Bundle
  const webviewCtx = await esbuild.context({
    entryPoints: ['src/webview/viewer.ts'],
    bundle: true,
    format: 'iife',
    minify: isProduction,
    sourcemap: !isProduction,
    sourcesContent: false,
    platform: 'browser',
    outfile: 'dist/webview.js',
    logLevel: 'info',
    plugins: [emptyNodeModulesPlugin],
    define: {
      'process.env.NODE_ENV': isProduction ? '"production"' : '"development"',
    },
  });

  if (isWatch) {
    await extensionCtx.watch();
    await webviewCtx.watch();
    console.log('[build] Watching for changes...');
  } else {
    await extensionCtx.rebuild();
    await webviewCtx.rebuild();
    await extensionCtx.dispose();
    await webviewCtx.dispose();
    console.log('[build] Completed successfully!');
  }
}

build().catch((e) => {
  console.error('[build] Failed:', e);
  process.exit(1);
});
