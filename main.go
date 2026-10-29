
package main

import (
	"crypto/rand"
	"errors"
	"flag"
	"fmt"
	"math/big"
	"os"
	"os/exec"
	"strings"
)

const (
	lowercase = "abcdefghijklmnopqrstuvwxyz"
	uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	digits   = "0123456789"
	special  = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
	letters  = lowercase + uppercase
)

func randomInt(max int) (int, error) {
	n, err := rand.Int(rand.Reader, big.NewInt(int64(max)))
	if err != nil {
		return 0, err
	}
	return int(n.Int64()), nil
}

func randomChar(charset string) (byte, error) {
	n, err := randomInt(len(charset))
	if err != nil {
		return 0, err
	}
	return charset[n], nil
}

func generatePassword(length int, charsets []string) (string, error) {
	if length <= 0 {
		return "", errors.New("length must be greater than zero")
	}

	if length < len(charsets) {
		return "", fmt.Errorf(
			"password length must be at least %d for the selected character types",
			len(charsets),
		)
	}

	// Объединяем все выбранные наборы символов.
	allChars := strings.Join(charsets, "")

	password := make([]byte, length)

	// Добавляем по одному символу каждого выбранного типа.
	for i, charset := range charsets {
		ch, err := randomChar(charset)
		if err != nil {
			return "", err
		}
		password[i] = ch
	}

	// Заполняем оставшуюся часть пароля.
	for i := len(charsets); i < length; i++ {
		ch, err := randomChar(allChars)
		if err != nil {
			return "", err
		}
		password[i] = ch
	}

	// Перемешиваем пароль криптографически стойким способом.
	for i := len(password) - 1; i > 0; i-- {
		j, err := randomInt(i + 1)
		if err != nil {
			return "", err
		}
		password[i], password[j] = password[j], password[i]
	}

	return string(password), nil
}

func copyToClipboard(password string) error {
	// Wayland / Niri.
	if wlCopy, err := exec.LookPath("wl-copy"); err == nil {
		cmd := exec.Command(wlCopy)
		cmd.Stdin = strings.NewReader(password)

		if err := cmd.Run(); err == nil {
			return nil
		}
	}

	// X11 fallback.
	if xclip, err := exec.LookPath("xclip"); err == nil {
		cmd := exec.Command(
			xclip,
			"-selection",
			"clipboard",
		)
		cmd.Stdin = strings.NewReader(password)

		if err := cmd.Run(); err == nil {
			return nil
		}
	}

	return errors.New(
		"clipboard utility not found; install wl-clipboard or xclip",
	)
}

func main() {
	length := flag.Int(
		"l",
		12,
		"Length of generated password",
	)

	copyFlag := flag.Bool(
		"c",
		false,
		"Copy generated password to clipboard",
	)

	hide := flag.Bool(
		"H",
		false,
		"Hide generated password",
	)

	digitsOnly := flag.Bool(
		"d",
		false,
		"Digits only",
	)

	lowercaseOnly := flag.Bool(
		"lowercase",
		false,
		"Lowercase letters only",
	)

	uppercaseOnly := flag.Bool(
		"U",
		false,
		"Uppercase letters only",
	)

	specialOnly := flag.Bool(
		"s",
		false,
		"Special characters only",
	)

	lettersOnly := flag.Bool(
		"L",
		false,
		"Letters only",
	)

	flag.Parse()

	// Выбираем типы символов.
	var charsets []string

	if *digitsOnly {
		charsets = append(charsets, digits)
	}

	if *lowercaseOnly {
		charsets = append(charsets, lowercase)
	}

	if *uppercaseOnly {
		charsets = append(charsets, uppercase)
	}

	if *specialOnly {
		charsets = append(charsets, special)
	}

	if *lettersOnly {
		charsets = append(charsets, letters)
	}

	// Если типы не выбраны, используем стандартный набор.
	if len(charsets) == 0 {
		charsets = []string{
			digits,
			uppercase,
			lowercase,
			special,
		}
	}

	password, err := generatePassword(
		*length,
		charsets,
	)

	if err != nil {
		fmt.Fprintln(os.Stderr, "Error:", err)
		os.Exit(1)
	}

	// Выводим пароль.
	if *hide {
		fmt.Println("pass-gen:" + strings.Repeat("*", len(password)))
	} else {
		fmt.Println(password)
	}

	// Копируем пароль в буфер обмена.
	if *copyFlag {
		if err := copyToClipboard(password); err != nil {
			fmt.Fprintln(os.Stderr, "Clipboard error:", err)
			os.Exit(1)
		}
	}
}
