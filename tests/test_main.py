import main


def test_show_items_prints_objects(capsys):
    main.show_items(["первый", "второй"])

    assert capsys.readouterr().out.splitlines() == ["первый", "второй"]


def test_show_items_handles_empty_collection(capsys):
    main.show_items([])

    assert capsys.readouterr().out


def test_main_exits_on_zero(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    main.main()

    assert "0 exit" in capsys.readouterr().out
