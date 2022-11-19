import typer


def main(name: str, lastname: str, formal: bool = False) -> None:
    if formal:
        print(f"Good morning {name} {lastname}")
    else:
        print(f"Hello {name} {lastname}")


if __name__ == "__main__":
    typer.run(main)
