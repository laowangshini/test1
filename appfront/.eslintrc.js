module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended"
  ],
  parserOptions: {
    parser: "@babel/eslint-parser",
  },
  rules: {
    "no-console": "off",
    "no-debugger": "off",
    "vue/multi-word-component-names": "off",
    "vue/no-multiple-template-root": "off",
    "vue/no-v-model-argument": "off",
    "vue/no-v-for-template-key": "off",
    "prettier/prettier": "off",
    "no-unused-vars": "off",
    "vue/no-unused-components": "off",
    "vue/no-parsing-error": "off",
    "vue/valid-template-root": "off",
    "vue/require-v-for-key": "off",
    "vue/valid-v-for": "off",
    "vue/no-use-v-if-with-v-for": "off",
    "vue/no-dupe-keys": "off",
    "vue/no-template-key": "off",
    "vue/no-unused-vars": "off",
    "vue/no-mutating-props": "off",
    "vue/require-prop-type-constructor": "off",
    "vue/require-default-prop": "off",
    "vue/no-side-effects-in-computed-properties": "off"
  },
};
