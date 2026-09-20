# -*- coding: utf-8 -*-
import ast


def line_number(file_name: str, new_file_name: str) -> None:
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(new_file_name, "w", encoding="utf-8") as new_file:
            for i, line in enumerate(lines, 1):
                new_file.write(f"{i}. {line}")

    except OSError as error:
        print(f"There was a problem with the file: {error}")
        raise


def parse_functions(file_name: str) -> tuple:
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            code = file.read()

        tree = ast.parse(code)
        functions = []

        for item in tree.body:
            if isinstance(item, ast.FunctionDef):
                line_num = item.lineno
                function_name = item.name
                arguments = ast.unparse(item.args)
                function_code = ast.unparse(item)

                functions.append(
                    (
                        line_num,
                        function_name,
                        arguments,
                        function_code,
                    )
                )

        functions.sort(key=lambda x: x[1])

        return tuple(functions)

    except (OSError, SyntaxError) as error:
        print(f"There was a problem reading the Python file: {error}")
        raise


def main() -> None:
    file_name = "p1_Fornaro_Brian.py"
    new_file_name = "p1_numbered.txt"

    line_number(file_name, new_file_name)

    functions = parse_functions(file_name)

    print("Functions found:")
    print(functions)


if __name__ == "__main__":
    main()