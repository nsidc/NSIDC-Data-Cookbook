# How to Publish Cookbook on GH Pages

I am following these [instructions](https://quarto.org/docs/publishing/github-pages.html#github-action) provided by Quarto.

## 1. Freeze Computations

I am only allowing code to be executed locally.

In `_quarto.yml`, I have added the following
```
execute:
  freeze: auto
```

Now render the site
```
quarto render
```

If a `_freeze` directory is created, add and commit this.

## 2. Publish Action

Run

```
quarto publish gh-pages
```

Add `.github/workflows/publish.yml` and add text from quarto [instructions](https://quarto.org/docs/publishing/github-pages.html#publish-action)

