module.exports = {
  important: true,
  content: [
    "./job_board/templates/**/*.html",
    "./job_board/static/sass/**/*.scss",
    "./job_board/static/js/**/*.js",
  ],
  //   darkMode: false, // or 'media' or 'class'
  variants: {
    extend: {},
  },
  plugins: [],
  prefix: "tw-",
  theme: {
    extend: {
      flexGrow: {
        '2': 2
      },
      flexShrink: {
        '2': 2
      }
    },
    screens: {
      sm: "576px",
      md: "768px",
      lg: "992px",
      xl: "1200px",
    },
  },
};
