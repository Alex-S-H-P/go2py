package example

func Func1(i int) int {
	return i + i
}

func Func2(j, k string) string {
	return ""
}

type MyStruct struct {
	field1 string
	field2 int
	field3 []int
	field4 struct {
		field41 int
		field42 [3]int
	}
}

func Func3(s MyStruct) (string, int, error) {
	return s.field1, s.field2, nil
}

func Func4(s MyStruct) int {
	return len(s.field3) + s.field4.field41 + s.field4.field42[1]
}
