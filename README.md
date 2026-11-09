![SMASSH](imgs/smassh_banner.png)

# Smassh 🖮

Smassh is a TUI based typing test application inspired by MonkeyType \
-- A very popular online web-based typing application

Smassh tries to be a full fledged typing test experience but not missing
out on looks and feel!

[![GitHub issues](https://img.shields.io/github/issues/kraanzu/smassh?color=red&style=for-the-badge)](https://github.com/kraanzu/smassh/issues)
[![GitHub stars](https://img.shields.io/github/stars/kraanzu/smassh?color=green&style=for-the-badge)](https://github.com/kraanzu/smassh/stargazers)
[![GitHub license](https://img.shields.io/github/license/kraanzu/smassh?color=yellow&style=for-the-badge)](https://github.com/kraanzu/smassh/blob/main/LICENSE)
[![Support Server](https://img.shields.io/discord/989186205025464390.svg?label=Discord&logo=Discord&colorB=7289da&style=for-the-badge)](https://discord.gg/WA2ER9MBWa)

> [!CAUTION]
> Smassh, by default, uses [nerd fonts](https://www.nerdfonts.com/) for the icons
> If not installed, you'll see random gibberish icons

# Installation 🔨

## Using Pip 🐍

> You can install the stable version of smassh by using pip or [pipx](https://github.com/pypa/pipx)

```bash
pip install smassh
```

## Using AUR 📦

```
yay -S smassh-bin
```

### Executable binary 🔌

You should be able to see binaries for `Linux`, `mac` and `windows` in the [releases section](https://github.com/kraanzu/smassh/releases)

> [!NOTE]
> This should automatically create an executable `smassh` that can be directly run from command line \
> If not, check if the local path is added to `$PATH`

# Features 🌟

> Some features that smassh comes with:

- An interactive & beautiful UI
- Words and Time modes for typing
- Real-time comparison of speed carets
- Change styles/settings on the fly
- Mutliple theme support
- Mutliple language support
- Lots of options to tweak!

# Tweaks ⚙️

| Tweak           | Description                                                                  |
| --------------- | :--------------------------------------------------------------------------- |
| Blind mode      | You wouldn't be able to see your mistakes                                    |
| Capital Letters | Some letters in your tasks will be capitalized!                              |
| Caret Style     | Caret style matters!                                                         |
| Confidence mode | Are you sure you don't need backspace? Try this :)                           |
| Cursor Buddy    | Setup your cursor buddy to run along with you!                               |
| Difficulty      | Choose how strict smassh should be with your wrong keypresses                |
| Force Correct   | You wouldn't be able to able to go on without cleaning your pool of mistakes |
| Min Accuracy    | Fall below this average accuracy and you fail!                               |
| Min Burst       | Fall below this average accuracy for even a word and you fail!               |
| Min Speed       | Fall below this average speed and you fail!                                  |
| Tab Reset       | Hey hey! You wanna reset already? I got ya!                                  |

# Screenshots 🖼️

![github](imgs/preview.png)

# Contribution 🤝

See [CONTRIBUTING.md](CONTRIBUTING.md) for contributions

# Credits 
[@frizd](https://github.com/frizd) for the awesome banner \
[@miodec](https://github.com/Miodec) for monkeytype!

# Other TUI projects 🤓 :

If you liked smassh then you might wanna try out some of my other TUI projects as well

- [dooit](https://github.com/kraanzu/dooit) - A todo app that you didn't ask for but needed!
- [gupshup](https://github.com/kraanzu/gupshup) - A localhost TUI chat client

## Local progress

Results are saved automatically in `smassh.json` in the platform's user data
folder for smassh. Open **progress** in the header or press `Ctrl+G` to see the
history, horizontal WPM bars with exact values, accuracy and test counts. Each
bar shows the average of successful attempts for a calendar week (Monday–Sunday);
period filters include only attempts within the selected period. Choose
**Horizontal bars** or **Line chart** using the chart selector. Both views use
the same weekly averages; the line view shows speed and accuracy separately.
Filter by the current test settings or view all attempts, and choose a time period. Failed attempts remain in the history but do
not contribute to records or averages. Older results without language and
modifier information are available under **All attempts**.

The result screen compares each test with previous successful tests using the
same mode, limit, language and difficulty settings. Speed calculations follow
smassh's existing metrics.

Use **Clear history** (or `C` on the progress screen) to remove all saved attempts.
The confirmation dialog allows cancellation; clearing does not change settings,
installed languages or themes. This action cannot be undone.
