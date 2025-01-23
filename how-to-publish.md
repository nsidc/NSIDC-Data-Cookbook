# How to Publish Cookbook on GH Pages

I am following these [instructions](https://quarto.org/docs/publishing/github-pages.html#github-action) provided by Quarto.

## 1. Freeze Computations

I am only allowing code to be executed locally.

In `_quarto.yml`, I have added the following
```
execute:
  freeze: auto
```
