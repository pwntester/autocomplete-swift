# autocomplete-swift

[![License][license-badge]][license]
[![Release][release-badge]][release]

Autocompletion for Swift in [NeoVim][web-neovim] with [deoplete][github-deoplete].

![completion-gif](/_images/completion.gif)


## Announcement

- **Autocompletion-swift dropped support for Vim and completion with omni-function**. Please use this plugin in NeoVim with deoplete.nvim.
- This plugin adopted [Yata][github-yata] instead of SourceKitten and SourceKittenDaemon.


## Installation

Autocomplete-swift uses [Yata][github-yata] as its back-end.
Therefore this plugin supports macOS only.
Yata can be installed with [Homebrew][github-homebrew].

Please execute the following command:

```bash
$ brew tap mitsuse/yata
$ brew install yata
```

To install autocomplete-swift,
it is recommended to use plugin manager such as [dein.vim][github-dein].
In the case of dein.vim, please add the following codes into `init.vim` and configure them:

```vim
call dein#add('Shougo/deoplete.nvim')
call dein#add('mitsuse/autocomplete-swift')
```

This plugin also supports jumping to placeholders in arguments of method.
The following configuration is required:

```vim
" Jump to the first placeholder by typing `<C-k>`.
autocmd FileType swift imap <buffer> <C-k> <Plug>(autocomplete_swift_jump_to_placeholder)
```

If you use [neosnippet][github-neosnippet],
you should enable [key-mappings of neosnippets][github-neosnippet-config] instead of using the above code.
Autocomplete-swift gets along with neosnippet by converting placeholders into its ones.


## Usage

First, run Yata server in your shell:

```text
$ yata run --port 9000 # Choose a port number.
```

After that, execute `:call yata#enable(9000)` in NeoVim.
Pass the same port number as one used by Yata to this function.


## Features

### Completion

Autocomplete-swift supports types of completion as follow:

- Type name
- Type/Instance member
- Function/method/initializer parameter
- Top-level function/constant/variable
- Keyword such as `protocol`, `extension` etc.
- Method definition


### Placeholder

This plugin supports jumping to placeholders in arguments of method.
Please read [Installation](#installation).


## TODO

- Display more information of candidate (For example, the kind of candidate etc).
- Make configurable. For example, autocomplete-swift will get `max_candiates` for neocomplete from a variable.
- Add support for Linux.


## Related project

In the GIF on the beginning,
I use snippets for Swift contained in [neosnippet-snippets][github-neosnippet-snippets]
in addition to autocomplete-swift.


## License

Please read [LICENSE][license].

[license-badge]: https://img.shields.io/badge/license-MIT-yellowgreen.svg?style=flat-square
[license]: LICENSE
[release-badge]: https://img.shields.io/github/tag/mitsuse/neocomplete-swift.svg?style=flat-square
[release]: https://github.com/mitsuse/neocomplete-swift/releases
[github-yata]: https://github.com/mitsuse/yata
[github-homebrew]: https://github.com/Homebrew/homebrew-core
[github-neosnippet]: https://github.com/Shougo/neosnippet.vim
[github-neosnippet-config]: https://github.com/Shougo/neosnippet.vim#configuration
[github-neosnippet-snippets]: https://github.com/Shougo/neosnippet-snippets
[github-deoplete]: https://github.com/Shougo/deoplete.nvim
[github-dein]: https://github.com/Shougo/dein.vim
[web-neovim]: https://neovim.io/
