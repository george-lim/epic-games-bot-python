from hello_bot import HelloBot


def test_print_hello_message(capsys):
    name = "George"
    bot = HelloBot(name)

    bot.print_hello_message()

    out, err = capsys.readouterr()
    assert out == f"Hello {name}!\n"
    assert err == ""


def test_is_valid_url_reachable():
    is_url_reachable = HelloBot.is_url_reachable("https://george-lim.github.io")
    assert is_url_reachable


def test_is_invalid_url_reachable():
    is_url_reachable = HelloBot.is_url_reachable(
        "https://george-lim.github.io/aoaosdhgoasndgiuh"
    )

    assert not is_url_reachable
