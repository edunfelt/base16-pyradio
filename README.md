# base16-pyradio
This repo contains a set of theme files and templates for internet radio player [pyradio](https://github.com/coderholic/pyradio) meant to work with any [base16 builder](https://github.com/base16-project/base16).

Prebuilt themes have been built using [base16-builder-python](https://github.com/InspectorMustache/base16-builder-python), and can be found in the `themes/` directory. For detailed build and installation instructions, see [Installation](#installation).

## Installation
### Install a theme
To install individual themes, copy the desired `.pyradio-theme`-file in `themes/` to `~/.config/pyradio/themes/`, or use `curl`:

```
mkdir -p ~/.config/pyradio/themes
curl https://raw.githubusercontent.com/edunfelt/base16-pyradio/master/themes/base16-default-dark.pyradio-theme -o ~/.config/pyradio/themes/base16-default-dark.pyradio-theme
```

### Build themes
#### Requirements
- [base16-builder-node](https://github.com/base16-project/base16-builder-node)
- [Make](https://www.gnu.org/software/make/)

#### Instructions
```
git clone git@github.com:edunfelt/base16-pyradio.git
cd base16-pyradio
make
```

## Contributing
Contributions are welcome and greatly appreciated!

## Screenshots
**cupcake**

![cupcake](assets/cupcake.png)

**nord**

![nord](assets/nord.png)

**catppuccin**

![catppuccin](assets/catppuccin.png)

**everforest**

![everforest](assets/everforest.png)

**solarized-dark**

![solarized-dark](assets/solarized.png)
