import preprocess from 'svelte-preprocess';
import { vitePreprocess } from '@sveltejs/kit/vite';
import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: [
		vitePreprocess({
			postcss: true,
			defaults: {
				style: 'postcss'
			},
			scss: {
				includePaths: ['src/styles']
			}
		}),
		preprocess({
			postcss: true
		})
	],
	kit: {
		// paths: { assets: "", base: "/precog" },
		adapter: adapter({
			// default options are shown
			pages: 'build',
			assets: 'build',
			fallback: null,
			trailingSlash: 'always',
			// strict: false,
		})
	}
};

export default config;
