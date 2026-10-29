# PassGen

A simple command-line password generator written in Go.

## Features

- Cryptographically secure password generation
- Custom password length
- Selectable character types
- Copy password to clipboard (Wayland / X11)
- Hidden password output

## Installation

Build from source:

```bash
go build -o passgen main.go
```

Install globally:

```bash
sudo install -m 755 passgen /usr/local/bin/passgen
```

## Usage

```bash
passgen [options]
```

| Option | Description |
|---|---|
| `-l` | Password length (default: 12) |
| `-c` | Copy password to clipboard |
| `-H` | Hide password output |
| `-d` | Digits only |
| `--lowercase` | Lowercase letters only |
| `-U` | Uppercase letters only |
| `-s` | Special characters only |
| `-L` | Letters only |

Examples:

```bash
passgen
passgen -l 24
passgen -l 32 -c -H
passgen -l 16 -d -U -s
```

## Dependencies

- Go
- `wl-clipboard` (Wayland)
- `xclip` (X11, optional)

## License

MIT
