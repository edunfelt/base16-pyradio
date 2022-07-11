# base16-pyradio
This repo contains 4 sets of theme files and templates for internet radio player [pyradio](https://github.com/coderholic/pyradio) meant to work with any [base16 builder](https://github.com/base16-project/base16).

Prebuilt themes have been built using [base16-builder-node](https://github.com/base16-project/base16-builder-node), and can be found in the `themes/` directory. For detailed build and installation instructions, see [Installation](#installation).

## Installation
### Install a theme manually
To install individual themes, copy the desired `.pyradio-theme`-file in any of the directories under `themes/` to `~/.config/pyradio/themes/`, or use `curl`:

```
mkdir -p ~/.config/pyradio/themes
curl https://raw.githubusercontent.com/edunfelt/base16-pyradio/master/themes/default/base16-default-dark.pyradio-theme -o ~/.config/pyradio/themes/base16-default-dark.pyradio-theme
```

### Using the themes without base16-shell

The best way to use the themes is to install and set up [base16-shell](https://github.com/base16-project/base16-shell), (in which case no theme installation is necessary), but this is not mandatory.

To use the themes (without installing and using **base16-shell**) one would just have to clone this repo (or download the zip file), and copy the themes to `~/.config/pyradio/themes`.

One might just want to test the themes, by copying one of the directories to `~/.config/pyradio/themes`, for example

    cp themes/variation/* ~/.config/pyradio/themes

to "install" and test the variation set of the themes.

Consecutive use of this command (using a different source directory) will just overwrite any previously copied themes.

To copy all the themes, just use the following script.

**Notice:** this will copy more than **900 files** in the target directory... You've been warned...

**copy-themes**
```
#!/bin/bash
if [ $(basename "$PWD") != "themes"  ]
then
    echo "Run this script in the \"themes\" dir only!"
    exit 1
fi
TARGET=~/.config/pyradio/themes
mkdir -p "${TARGET}"

for ADIR in default default-alt variation variation-alt
do
    cd "${ADIR}"
    for AFILE in *
    do
        \cp "${AFILE}"  "${TARGET}/${AFILE/.pyradio-theme/-$ADIR.pyradio-theme}"
    done
    cd ..
done

echo "All themes copied to: ${TARGET}"
```

### Build themes
#### Requirements

- [base16-builder-node](https://github.com/base16-project/base16-builder-node)
- [Make](https://www.gnu.org/software/make/)

#### Instructions

```
mkdir -p base16/templates && cd base16/templates
git clone git@github.com:edunfelt/base16-pyradio.git
cd base16-pyradio
make
```


## Cycling through the themes

To see all the themes provided by this repo, follow this procedure:

Create a new file anywhere in you PATH, in `~/.lobal/bin` for example, and name it `cycle_base16_themes`.

```
touch ~/.local/bin/cycle_base16_themes
```

Open it in a text editor and paste the following in it:

```
#!/bin/bash
if [ $(basename "$PWD") != "themes"  ]
then
    echo "Run this script in the \"themes\" dir only!"
    exit 1
fi

mkdir -p ~/.config/pyradio/themes
\cp default/base16-3024.pyradio-theme ~/.config/pyradio/themes/cycle_base16_themes.pyradio-theme

clear
echo "Please execute PyRadio now and \"watch\" the \"cycle_base16_themes\" theme

To do that:
  1. Press \"t\" to open the \"Themes Selection\" window
  2. Select the \"cycle_base16_themes\" entry
  3. Press \"c\" to watch it
  4. Press \"ESCAPE\" to close the \"Themes Selection\" window
"
echo -n "When you are ready, please press \"ENTER\" to continue..."
read

ALL=$(ls -1 default/*.pyradio-theme | wc -l)
ALL=$((ALL * 4))
while true
do
    clear
    COUNT=1
    for n in default/*.pyradio-theme
    do
        echo -n '-'
        printf '%3s/%s. ' $COUNT $ALL
        echo "${n/.*/}"
        # echo $k/${n/.*/}
        ((COUNT++))
        \cp "$n" ~/.config/pyradio/themes/cycle_base16_themes.pyradio-theme
        sleep 2.5
        for k in default-alt variation variation-alt
        do
            printf '%4s/%s. ' $COUNT $ALL
            f="$k"/$(basename "$n")
            echo "${f/.*/}"
            ((COUNT++))
            \cp "$f" ~/.config/pyradio/themes/cycle_base16_themes.pyradio-theme
            sleep 2.5
        done

    done
    echo "All done... Repeating in 5 seconds!"
    sleep 5
done
```

Finally, make it executable:

```
chmod +x ~/.local/bin/cycle_base16_themes
```

Obviously, you will have to use the file location you used when you created the file.

Execute it in a terminal... and follow the instructions.

Enjoy!


## Contributing

Contributions are welcome and greatly appreciated!


## Screenshots
Left side shows the `default` themes, right side shows `variant` themes.

**cupcake**

<p align="center">
    <img src="assets/cupcake.png" width="45%" />
    <img src="assets/cupcake-variant.png" width="45%" />
</p>

**nord**

<p align="center">
    <img src="assets/nord.png" width="45%" />
    <img src="assets/nord-variant.png" width="45%" />
</p>

**catppuccin**

<p align="center">
    <img src="assets/catppuccin.png" width="45%" />
    <img src="assets/catppuccin-variant.png" width="45%" />
</p>


**solarized-dark**

<p align="center">
    <img src="assets/solarized-dark.png" width="45%" />
    <img src="assets/solarized-dark-variant.png" width="45%" />
</p>


**solarized-light**

<p align="center">
    <img src="assets/solarized-light.png" width="45%" />
    <img src="assets/solarized-light-variant.png" width="45%" />
</p>
