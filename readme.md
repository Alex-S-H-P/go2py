# Go2Py

## Limitations

The following limitations indicate the limits of the programs as it stands now. It is our goal to fix every single one of them in due time.

- **All functions to be detected must be unindented**.
- **No function to be skipped (lambdas, etc...) can be unindented**.
- **All files of a same package must be in the same directory**
- **The files `__go2py_wrappers.go`, and either `__go2py_wrappers.so` and `__go2py_wrappers.dll`** (on UNIX-based systems and windows respectly) **must be free**
- **Function args** in the definition **must not include parenthesis**
- **Symbols to be detected cannot be generic**
- **Valid value types** (values including arguments, returned values, and fields) are:
  - `string`
  - `int`
  - `byte`
  - `float32`
  - `bool`
  - a `slice` of a valid value type
  - an `array` of a valid value type

## Conversions

| go type    | | | | | python equivalent          |
|:-----------|-|-|-|-|---------------------------:|
| `string`   | | | | | `str`                      |
| `int`      | | | | | `int`                      |
| `float32`  | | | | | `float`                    |
| `byte`     | | | | | `int`                      |
| `bool`     | | | | | `bool`                     |
| `slice`    | | | | | `sequence`                 |
| `array`    | | | | | `sequence` of same `len()` |
| `[]byte`   | | | | | can be passed as a `str`   |
