import presetWebFonts from '@unocss/preset-web-fonts'
import presetUno from '@unocss/preset-uno'
import UnoCSS from 'unocss/vite'

export default UnoCSS({
  presets: [
    presetUno(),
    presetWebFonts({
      provider: 'google',
      fonts: {
        sans: 'Roboto:400,700',
        mono: ['Roboto Mono:400,700'],
      },
    }),
  ],
})