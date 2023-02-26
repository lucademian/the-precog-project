import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import UnoCSS from './src/lib/uno'

export default defineConfig({
	plugins: [UnoCSS, sveltekit()]
});
