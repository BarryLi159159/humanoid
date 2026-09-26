## Contributing

All tables are generated from `data/*.yaml`. To add or fix a paper:

1. Edit the relevant YAML file (fields: `id`, `name`, `title`, `venue`, `depth`, `novelty`, `limitation`; add `link` and `date` for non-arXiv entries).
2. Run `pip install pyyaml && python scripts/build_readme.py`.
3. Open a PR. Upgrading a † entry to `depth: A` after reading the paper, or confirming a venue, is especially welcome.

The build script validates required fields, duplicate IDs, and the 2025-01 scope cutoff.

## License

Text and data: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Script: MIT.
