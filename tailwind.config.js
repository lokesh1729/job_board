module.exports = {
  important: true,
  content: [
    './job_board/templates/**/*.html',
    './job_board/static/sass/**/*.scss',
    './job_board/static/js/**/*.js'
  ],
  //   darkMode: false, // or 'media' or 'class'
  variants: {
    extend: {}
  },
  plugins: [],
  prefix: 'tw-',
  theme: {
    extend: {
      colors: {
        blue: {
          600: '#176DFC'
        }
      },
      flexGrow: {
        2: 2
      },
      flexShrink: {
        2: 2
      },
      width: {
        68: '17rem',
        70: '17.5rem'
      }
    }
  }
};
