<p align="center">
  <img src="https://raw.githubusercontent.com/souloss/souloss/output/snake.svg" alt="SOULOSS GitHub contribution snake" width="100%">
  <img src="https://raw.githubusercontent.com/souloss/souloss/output/recent.svg" alt="Recently updated public repositories" width="100%">
</p>

## Profile panel

This repository builds small, self-contained SVG cards for the GitHub profile. The first version has a contribution snake and a recent repositories card. Source code and generated images live on separate branches: `master` contains the renderer; GitHub Actions publishes `dist/` to `output`.

### Customize

Edit [`config/profile.toml`](config/profile.toml) to change the GitHub account, timezone, colors, repository count, or excluded repositories. The repository list uses GitHub's public REST API; no personal access token is needed for public data. GitHub Actions supplies its job token to improve the API rate limit.

The contribution snake is produced by [Platane/snk](https://github.com/Platane/snk) in the workflow and then placed in the same panel frame as the other card.

### Develop locally

Use Python 3.11 or newer. The recent repositories card can be rendered with:

```sh
python scripts/generate.py dist
```

To add a card, keep its data fetching in a provider, convert the response into a small plain-data structure, and add a renderer in `scripts/cards.py` that returns a complete SVG. Shared colors, XML escaping, and the outer SVG document live in `scripts/theme.py`. Add the generated filename to `README.md` and the workflow's publish output as needed.

The scheduled workflow refreshes the panel daily. It restores the last published render before fetching, so a failed data request does not replace the existing card with a broken image.
